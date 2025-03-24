import subprocess
import re
import sys
import os
import time
from tqdm import tqdm
from modules.functions import update_progress, convert_time_to_seconds, extract_video_id
import math
import yt_dlp
from typing import Dict, Any, List, Callable, Optional
import functools

comment_pattern = r"\[youtube\] Downloading comment (.+)"
page_pattern = r"page (\d+)"
count_pattern = r"\((\d+)\/~(\d+)\)"
youtube_download = r'\[(?P<label>download)\]\s+(?P<percentage>\d*\.?\d+)%'
error_pattern = r"ERROR: \[youtube\] (?P<video_id>[-\w]+): (?P<error_message>.+)"


def run_subprocess(command):
    """
    The function `run_subprocess` runs a command as a subprocess and returns the output.

    :param command: The `command` parameter is a string that represents the command you want to run in
    the subprocess. It can be any valid command that you would normally run in a terminal or command
    prompt
    :return: a subprocess.Popen object.
    """
    return subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
    )


def handle_conversion_interrupted(process, progress_bar, output_file):
    """
    The function handles the case when a conversion process is interrupted by the user.

    :param process: The process parameter refers to the running process that is being interrupted. It
    could be a subprocess or a thread that is responsible for performing the conversion task
    :param progress_bar: The `progress_bar` parameter is an object that represents a progress bar. It is
    used to display the progress of the conversion process to the user
    :param output_file: The `output_file` parameter is the file path of the output file that is being
    generated during the conversion process
    """
    print("Conversion interrupted by user.")
    progress_bar.close()
    process.terminate()
    if os.path.exists(output_file):
        os.remove(output_file)
    sys.exit(1)


def handle_error(e, process, progress_bar, output_file):
    """
    The function "handle_error" is used to handle errors by printing the error message, closing the
    progress bar, terminating the process, deleting the output file if it exists, and exiting the
    program with a status code of 1.

    :param e: The parameter "e" is the exception object that represents the error that occurred. It is
    used to print the error message in the error handling function
    :param process: The "process" parameter refers to a running process or subprocess that you want to
    handle errors for. It could be a long-running task or a subprocess that you have started using the
    `subprocess` module
    :param progress_bar: The `progress_bar` parameter is an object that represents a progress bar. It is
    used to display the progress of a process or task
    :param output_file: The `output_file` parameter is the file path or name of the file where the
    output of the process is being written to
    """
    print("An error occurred:", str(e))
    if progress_bar:
        progress_bar.close()
    if process:
        process.terminate()
    if output_file and os.path.exists(output_file):
        time.sleep(5)
        os.remove(output_file)
    sys.exit(1)


def download_video(video_url: str, ytdlp_options: Dict[str, Any], video_id: str, total_videos: int, file_counter: int) -> bool:
    """
    Download a single video using YT-DLP with native progress reporting.

    :param video_url: The URL of the video to download
    :param ytdlp_options: Dictionary containing YT-DLP options
    :param video_id: The ID of the video being downloaded
    :param total_videos: Total number of videos to download
    :param file_counter: Current video number being processed
    :return: True if download was successful, False otherwise
    """
    try:
        # Print simple progress header
        print(f"\n[{file_counter}/{total_videos}] Downloading video: {video_id}")

        # Create a minimal set of options to avoid any potential conflicts
        minimal_options = {
            'format': ytdlp_options.get('format', 'best'),
            'outtmpl': ytdlp_options.get('outtmpl', 'downloads/%(extractor)s/%(id)s.%(ext)s'),
            'quiet': False,  # Ensure progress is shown
            'no_color': True,  # Disable colors which can cause issues
        }

        # Extract progress options
        progress_options = ytdlp_options.get('progress_options', {})

        # Add only essential options and safe progress options
        if 'cookiefile' in ytdlp_options:
            minimal_options['cookiefile'] = ytdlp_options['cookiefile']

        if 'writesubtitles' in ytdlp_options:
            minimal_options['writesubtitles'] = ytdlp_options['writesubtitles']
            minimal_options['subtitleslangs'] = ytdlp_options.get(
                'subtitleslangs', ['en'])

        if 'writethumbnail' in ytdlp_options:
            minimal_options['writethumbnail'] = ytdlp_options['writethumbnail']

        if 'embed_thumbnail' in ytdlp_options:
            minimal_options['embed_thumbnail'] = ytdlp_options['embed_thumbnail']

        if 'addmetadata' in ytdlp_options:
            minimal_options['addmetadata'] = ytdlp_options['addmetadata']

        if 'proxy' in ytdlp_options:
            minimal_options['proxy'] = ytdlp_options['proxy']

        # Handle safe progress options
        if progress_options.get('quiet', False):
            minimal_options['quiet'] = True

        if progress_options.get('verbose', False):
            minimal_options['verbose'] = True

        if progress_options.get('no_warnings', False):
            minimal_options['no_warnings'] = True

        if progress_options.get('simulate', False):
            minimal_options['simulate'] = True

        if progress_options.get('skip_download', False):
            minimal_options['skip_download'] = True

        # Create YT-DLP instance with minimal options
        with yt_dlp.YoutubeDL(minimal_options) as ydl:
            # Download the video
            ydl.download([video_url])

        print(
            f"Successfully downloaded [{file_counter}/{total_videos}]: {video_id}")
        return True

    except yt_dlp.utils.DownloadError as e:
        # Handle download errors
        print(f"Download error for {video_id}: {str(e)}")
        return False

    except Exception as e:
        # Handle other errors
        print(f"Unexpected error for {video_id}: {str(e)}")
        # Try with ultra minimal options if we have a type error
        if isinstance(e, TypeError) or "TypeError" in str(e):
            try:
                print("Attempting with ultra minimal options due to error...")
                ultra_minimal_options = {
                    'format': 'best',
                    'outtmpl': f'downloads/{video_id}.%(ext)s',
                    'quiet': False,
                    'no_color': True
                }
                with yt_dlp.YoutubeDL(ultra_minimal_options) as ydl:
                    ydl.download([video_url])
                print(
                    f"Successfully downloaded with ultra minimal options: {video_id}")
                return True
            except Exception as e2:
                print(f"Still failed with ultra minimal options: {str(e2)}")
                return False
        return False


def download_videos_from_source(source_type: str, source_config: Dict[str, Any],
                                ytdlp_options: Dict[str, Any], items: List[Dict[str, str]]):
    """
    Download videos from a specific source.

    :param source_type: The type of source (e.g., "youtube", "tiktok")
    :param source_config: The source-specific configuration from the media library
    :param ytdlp_options: Dictionary containing YT-DLP options
    :param items: List of items to download from the source
    """
    try:
        # Check for enabled flag
        if not source_config.get('enabled', True):
            print(f"Source {source_type} is disabled. Skipping.")
            return

        # Count total items
        total_items = len(items)
        if total_items == 0:
            print(f"No items found for {source_type}. Skipping.")
            return

        print(f"Starting download of {total_items} items from {source_type}")

        # Process each item in the source
        for index, item in enumerate(items, 1):
            # Get URL from item - depending on source type, URL is stored differently
            url = item.get('url', '')

            # Skip if no URL
            if not url:
                print(f"No URL found for item {index}. Skipping.")
                continue

            # Always extract video ID from URL
            video_id = extract_video_id(url) or f"{source_type}-item-{index}"

            # Use source-level options by default
            item_options = ytdlp_options.copy()

            # Backward compatibility for older format
            if 'options' in item and isinstance(item['options'], dict):
                # Log a deprecation warning
                print(
                    f"Warning: Item-level options are deprecated for {video_id}. Please move to source-level config.")

                # Still support the old format
                for key, value in item['options'].items():
                    if key == 'progress_options' and isinstance(value, dict):
                        item_options['progress_options'] = {
                            **(item_options.get('progress_options', {})),
                            **value
                        }
                    else:
                        item_options[key] = value

            # Download the video with configured options
            success = download_video(
                url, item_options, video_id, total_items, index)

            # Handle download result
            if not success:
                print(
                    f"Failed to download item {index}/{total_items}: {video_id}")

        print(f"Finished processing all items from {source_type}")

    except Exception as e:
        print(f"Error processing source {source_type}: {str(e)}")
        import traceback
        traceback.print_exc()
