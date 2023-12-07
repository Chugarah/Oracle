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
    return subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
    )


def get_file_info(process, video_id, total_link, file_counter):
    """
    The function `get_file_info` takes in a process and video ID, and uses regular expressions to
    extract information about the progress of downloading comments and videos, updating a progress bar
    accordingly.

    :param process: The `process` parameter is the subprocess that is running the command to download
    the file. It is used to read the output of the command and extract information about the progress of
    the download
    :param video_id: The `video_id` parameter is the unique identifier of the video that you want to get
    the file information for
    :return: the `progress_bar` object.
    """
    total_duration_var = None
    progress_bar = tqdm(total=100, position=0, leave=True, dynamic_ncols=True)
    enable_disable_flag = False
    for line in process.stdout:
        # print(line)
        matches_error_copyright = re.findall(error_pattern, line)
        for match in matches_error_copyright:
            # Assuming video_id is the first capturing group in your regex
            video_id = match[0]
            # Assuming error_message_not_available is the second capturing group
            error_message_not_available = match[1]
            # Check if there is an error message before printing
            if error_message_not_available:
                # Print an error message including the video ID
                progress_bar.close()
                print(
                    f"Error downloading video {video_id}: {error_message_not_available}")

            else:
                enable_disable_flag = True

        if not enable_disable_flag:
            matches_comments_downloading = re.findall(comment_pattern, line)
            for match in matches_comments_downloading:

                page_match = re.search(page_pattern, match)
                count_match = re.search(count_pattern, match)

                if page_match and count_match:
                    page_number = page_match.group(1)
                    current_count = int(count_match.group(1))
                    total_count = int(count_match.group(2))

                    # Set progressbar description
                    progress_bar.set_description(
                        f"Downloading comment from video {video_id}  ({file_counter}/{total_link}) page: {page_number}"
                    )
                    # Update progressbar
                    update_progress(progress_bar, current_count, total_count)

            # Match output for video download
            match_download_video = re.findall(youtube_download, line)
            for match in match_download_video:
                percentage = float(match[1])
                rounded_percentage = math.ceil(percentage)

                # Set progressbar description
                progress_bar.set_description(
                    f"Download video {video_id}: {file_counter}/{total_link}"
                )

                # Update progressbar
                update_progress(progress_bar, rounded_percentage, 100)

    return progress_bar


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
    progress_bar.close()
    process.terminate()
    if os.path.exists(output_file):
        time.sleep(5)
        os.remove(output_file)
    sys.exit(1)


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


def download_video(video_url, config, video_id, total_videos, file_counter):
    """
    The function `download_video` downloads a video from a given URL using yt-dlp, handles potential
    errors and interruptions, and provides progress updates.

    :param video_url: The `video_url` parameter is the URL of the video that you want to download. It
    should be a valid URL pointing to a video file
    :param config: The `config` parameter is the location of the configuration file for `yt-dlp.exe`.
    This file contains settings and options for the video download process
    :param video_id: The `video_id` parameter is a unique identifier for the video. It can be used to
    track the progress or status of the video download or perform any other operations related to the
    specific video
    """
    command = ["youtube/script/yt-dlp.exe",
               "--config-location", config['config'], video_url]

    # If the user has enabled authentication, add the cookie to the command
    if config['authentication'] == "true":
        command.append("--cookies")
        command.append(config['authCookie'])

    process = run_subprocess(command)
    progress_bar = get_file_info(
        process, video_id, total_videos, file_counter)

    try:
        try:
            # Placeholder for potentially additional code
            pass
        except KeyboardInterrupt:
            handle_conversion_interrupted(process, progress_bar)

        process.wait()
        process.terminate()
        progress_bar.close()
    except Exception as e:
        handle_error(e, process, progress_bar)
