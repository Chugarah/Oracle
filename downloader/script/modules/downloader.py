import subprocess
import re
import sys
import os
import time
from tqdm import tqdm
from modules.functions import update_progress, convert_time_to_seconds
import math

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


def download_progress_hook(progress_data, video_id, total_videos, file_counter):
    """
    Progress hook function for yt-dlp to track download progress

    :param progress_data: Dictionary containing progress information from yt-dlp
    :param video_id: The video ID being downloaded
    :param total_videos: Total number of videos to download
    :param file_counter: Current file number being downloaded
    """
    status = progress_data['status']

    # Initialize progress bar if not already initialized
    if not hasattr(download_progress_hook, 'progress_bar'):
        download_progress_hook.progress_bar = tqdm(
            total=100, position=0, leave=True, dynamic_ncols=True)

    progress_bar = download_progress_hook.progress_bar

    if status == 'downloading':
        # Set progress bar description for video download
        progress_bar.set_description(
            f"Download video {video_id}: {file_counter}/{total_videos}"
        )

        # Calculate percentage based on bytes if available
        if progress_data.get('total_bytes'):
            percentage = (
                progress_data['downloaded_bytes'] / progress_data['total_bytes']) * 100
            rounded_percentage = math.ceil(percentage)
            update_progress(progress_bar, rounded_percentage, 100)
        elif progress_data.get('total_bytes_estimate'):
            percentage = (
                progress_data['downloaded_bytes'] / progress_data['total_bytes_estimate']) * 100
            rounded_percentage = math.ceil(percentage)
            update_progress(progress_bar, rounded_percentage, 100)

    elif status == 'finished':
        # Close the progress bar when download is complete
        progress_bar.close()
        # Reset the progress bar for future downloads
        del download_progress_hook.progress_bar

    elif status == 'error':
        progress_bar.close()
        print(
            f"Error downloading video {video_id}: {progress_data.get('error', 'Unknown error')}")
        del download_progress_hook.progress_bar


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


def download_video(video_url, config, video_id, total_videos, file_counter):
    """
    The function `download_video` downloads a video from a given URL using yt-dlp, handles potential
    errors and interruptions, and provides progress updates.

    :param video_url: The `video_url` parameter is the URL of the video that you want to download. It
    should be a valid URL pointing to a video file
    :param config: The `config` parameter is the location of the configuration file for `yt-dlp`.
    This file contains settings and options for the video download process
    :param video_id: The `video_id` parameter is a unique identifier for the video. It can be used to
    track the progress or status of the video download or perform any other operations related to the
    specific video
    """
    # Use yt-dlp with progress hooks for tracking download progress
    from yt_dlp import YoutubeDL

    # Create progress hook with video context
    import functools
    progress_hook = functools.partial(download_progress_hook, video_id=video_id,
                                      total_videos=total_videos, file_counter=file_counter)

    # Configure yt-dlp options
    ydl_opts = {
        'config_location': config['config'],
        'progress_hooks': [progress_hook],
    }

    # If the user has enabled authentication, add the cookie to the options
    if config['authentication'] == "true":
        ydl_opts['cookiefile'] = config['authCookie']

    # Create YoutubeDL instance and download the video
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except KeyboardInterrupt:
        # Handle keyboard interrupt
        if hasattr(download_progress_hook, 'progress_bar'):
            download_progress_hook.progress_bar.close()
            del download_progress_hook.progress_bar
        print("Download interrupted by user.")
        sys.exit(1)
    except Exception as e:
        # Handle other exceptions
        if hasattr(download_progress_hook, 'progress_bar'):
            download_progress_hook.progress_bar.close()
            del download_progress_hook.progress_bar
        print(f"Error during download: {e}")
        sys.exit(1)
