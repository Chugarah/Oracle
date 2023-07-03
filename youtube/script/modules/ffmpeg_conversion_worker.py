import subprocess
import re
import sys
import os
import time
from tqdm import tqdm
from modules.functions import update_progress, convert_time_to_seconds

regex_duration = re.compile(r"Duration: (\d{2}:\d{2}:\d{2}\.\d{2})")
regex_time = re.compile(r"time=(\d{1,2}:\d{1,2}:\d{1,2}\.\d{2})")
get_extension = re.compile(r"#0, (.*?), to")


def get_file_info(process, file_name, file_counter, files_to_convert):
    total_duration_var = None
    progress_bar = tqdm(total=100, position=0, leave=True, dynamic_ncols=True)

    for line in process.stdout:
        # print(line)
        if match := regex_duration.search(line):
            total_duration_var = convert_time_to_seconds(
                match.group(1)
            )

        if match := get_extension.search(line):
            progress_bar.set_description(
                f"Converting file {file_counter} / {files_to_convert}: {file_name}"
            )

        if match := regex_time.search(line):
            current_value = convert_time_to_seconds(match.group(1))

            # If current_value is greater than total duration,
            # set progress bar to 100%
            if current_value > total_duration_var:
                progress_bar.update(100 - progress_bar.n)
            else:
                progress_bar.update(
                    (current_value/total_duration_var)*100 - progress_bar.n)

            progress_bar.refresh()

    return progress_bar


def handle_conversion_interrupted(process, progress_bar, output_file):
    print("Conversion interrupted by user.")
    progress_bar.close()
    process.terminate()
    if os.path.exists(output_file):
        os.remove(output_file)
    sys.exit(1)


def handle_error(e, process, progress_bar, output_file):
    print("An error occurred:", str(e))
    progress_bar.close()
    process.terminate()
    if os.path.exists(output_file):
        time.sleep(5)
        os.remove(output_file)
    sys.exit(1)


def run_subprocess(command: list) -> subprocess.Popen:
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding='utf-8'  # Specify encoding to handle special characters
        )
        return process
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with return code {e.returncode}")
    except subprocess.TimeoutExpired:
        print("Command timed out")


def convert_sound(webm_files, output_file, file_khz, file_name, files_to_convert, file_counter):
    command = [
        "ffmpeg", "-i", webm_files, "-vn", "-acodec", "libmp3lame",
        "-b:a", "320k", "-ac", "2", "-ar", file_khz, "-y",
        "-map_metadata", "0", "-id3v2_version", "3", output_file
    ]

    process = run_subprocess(command)

    progress_bar = get_file_info(
        process, file_name, file_counter, files_to_convert)

    try:
        try:
            # Placeholder for potentially additional code
            pass
        except KeyboardInterrupt:
            handle_conversion_interrupted(process, progress_bar, output_file)

        process.wait()
        process.terminate()
        progress_bar.close()
    except Exception as e:
        handle_error(e, process, progress_bar, output_file)
