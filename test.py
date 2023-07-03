def convert_time_to_seconds(time_str):
    """
    The function `convert_time_to_seconds` converts a time string in the format "HH:MM:SS" or "SS.MS" to
    the total number of seconds.

    :param time_str: The `time_str` parameter is a string representing a time value. It can be in one of
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


string = " 01:00:21.920"
print(convert_time_to_seconds(string))
