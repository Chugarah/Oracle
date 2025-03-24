from datetime import timedelta
import datetime
import os
import re
import subprocess


def datetime_to_float(d):
    """
    The function `datetime_to_float` converts a datetime object to a floating-point number representing
    the total number of seconds.

    :param d: d is a datetime object, which represents a specific date and time
    :return: the total number of seconds in the given datetime object as a floating-point number.
    """
    total_seconds = d.total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds


def update_progress(progress_bar, current_value, total_value):
    """
    The function updates the progress bar with the current value and total value.
    Works with both percentage values and time-based values.

    :param progress_bar: The progress bar object that you want to update
    :param current_value: The current value represents the current progress or value that you want to
    update in the progress bar. It could be a number indicating the progress percentage or any other
    value that represents the progress
    :param total_value: The total value represents the maximum value or the total number of steps in the
    progress bar. It is used to calculate the progress percentage and update the progress bar
    accordingly
    :return: the updated progress bar.
    """
    try:
        # Ensure values are properly converted to float before any operations
        try:
            total_value_float = float(total_value)
            progress_bar.total = total_value_float
        except (ValueError, TypeError):
            # If conversion fails, use a default value
            progress_bar.total = 100.0
            print(
                f"Warning: Could not convert total_value '{total_value}' to float")

        # Handle current_value based on its type
        try:
            if isinstance(current_value, (int, float)):
                current_float = float(current_value)
            elif isinstance(current_value, str):
                current_float = float(current_value)
            else:
                # For time-based values
                current_value_timedelta = timedelta(seconds=current_value)
                current_float = datetime_to_float(current_value_timedelta)

            # Ensure n is a number before comparison
            n_float = float(
                progress_bar.n) if progress_bar.n is not None else 0.0

            # Calculate difference and update
            diff = current_float - n_float
            if diff > 0:  # Only update if there's positive progress
                progress_bar.update(diff)

        except (ValueError, TypeError) as e:
            # If conversion fails, just refresh the bar without updating
            print(f"Progress value conversion error: {e}")

        progress_bar.refresh()
        return progress_bar
    except Exception as e:
        # Catch all other exceptions to prevent download from failing
        print(f"Progress update error: {e}")
        try:
            progress_bar.refresh()
        except:
            pass
        return progress_bar


def convert_time_to_seconds(time_str):
    """
    The function `convert_time_to_seconds` converts a time string in the format "HH:MM:SS" or "SS.MS" to
    the total number of seconds.

    :param time_str: The time_str parameter is a string representing a time value. It can be in one of
    the following formats:
    :return: the total time in seconds.
    """
    if ":" in time_str:
        time_parts = time_str.split(":")
        if len(time_parts) == 2:  # Only minutes and seconds
            minutes, seconds = time_parts
            total_seconds = int(minutes) * 60 + float(seconds)
        else:  # Hours, minutes, seconds, and milliseconds
            hours, minutes, seconds = time_parts
            total_seconds = int(hours) * 3600 + \
                int(minutes) * 60 + float(seconds)
    else:
        seconds, milliseconds = time_str.split(".")
        total_seconds = int(seconds) + int(milliseconds) / 1000
    return total_seconds


def extract_video_id(url):
    """
    The function `extract_video_id` takes a YouTube URL as input and returns the video ID extracted from
    the URL.

    :param url: The `url` parameter is a string that represents the URL of a YouTube video
    :return: The function `extract_video_id` returns the video ID extracted from the given URL. If a
    video ID is found in the URL, it is returned as a string. If no video ID is found, it returns
    `None`.
    """
    video_id = re.search(
        r"(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|shorts\/|watch\?v=|watch\?.+&v=))([^\/\?\&]+)", url)
    if video_id:
        return video_id.group(1)
    else:
        return None


def generate_youtube_url(video_id):
    """
    The function `generate_youtube_url` takes a YouTube video ID as input and returns a YouTube URL.

    :param video_id: The `video_id` parameter is a string that represents the ID of a YouTube video
    :return: The function `generate_youtube_url` returns the YouTube URL for the given video ID.
    """
    return f"https://www.youtube.com/watch?v={video_id}"


def is_text_file_empty(file_path):
    """
    The function checks if a text file is empty by comparing its size to zero.

    :param file_path: The file path is the location of the text file that you want to check if it is
    empty or not. It should be a string that specifies the path to the file, including the file name and
    extension. For example, "C:/Documents/myfile.txt" or "/home/user/myfile.txt
    :return: a boolean value indicating whether the text file at the given file path is empty or not.
    """
    return os.stat(file_path).st_size == 0


def create_file_if_not_exists(file_path):
    if os.path.exists(file_path):
        return 'File already exists'

    with open(file_path, 'w') as file:
        pass

    return 'File created successfully'


def check_lowest_expiry(file_path):
    # Read the contents of the text file and store them in a list
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Convert the strings in the list to integers
    numbers = [int(line.strip()) for line in lines]

    # Find the lowest value in the list
    lowest = min(numbers)

    # Convert the lowest value to a datetime object
    lowest_datetime = datetime.datetime.fromtimestamp(lowest)

    # Get the current time
    now = datetime.datetime.now()

    # Compare the lowest value with the current time and return True or False
    return lowest_datetime < now


def run_subprocess(command):
    """
    The function `run_subprocess` runs a command as a subprocess and returns the output.

    :param command: The `command` parameter is a string that represents the command you want to run in
    the subprocess. It can be any valid command that you would normally run in a terminal or command
    prompt
    :return: a tuple containing the output and the error (output, error)
    """
    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
    ) as process:
        output, error = process.communicate()
    return output, error


def read_file(file_path):
    """
    The function `read_file` reads the contents of a file and prints each line, or prints a message if
    the file is empty or does not exist.

    :param file_path: The file path is a string that specifies the location of the file you want to
    read. It should include the file name and extension. For example,
    "C:/Users/username/Documents/file.txt" or "data/file.csv"
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) == 0:
                print("The file is empty.")
            else:
                for line in lines:
                    print(line.strip())
    except FileNotFoundError:
        print("The file does not exist.")
