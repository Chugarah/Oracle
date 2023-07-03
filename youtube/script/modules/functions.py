from datetime import timedelta
import datetime
import re


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

    :param progress_bar: The progress bar object that you want to update
    :param current_value: The current value represents the current progress or value that you want to
    update in the progress bar. It could be a number indicating the progress percentage or any other
    value that represents the progress
    :param total_value: The total value represents the maximum value or the total number of steps in the
    progress bar. It is used to calculate the progress percentage and update the progress bar
    accordingly
    :return: the updated progress bar.
    """
    progress_bar.total = float(total_value)

    # Convert current_value to timedelta object
    current_value_timedelta = timedelta(seconds=current_value)

    # Convert current_value_timedelta to float with millisecond precision
    current_value_float = datetime_to_float(current_value_timedelta)
    progress_bar.update(current_value_float - progress_bar.n)
    progress_bar.refresh()

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
    video_id = re.search(
        r"(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|shorts\/|watch\?v=|watch\?.+&v=))([^\/\?\&]+)", url)
    if video_id:
        return video_id.group(1)
    else:
        return None
