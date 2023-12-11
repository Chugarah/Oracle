import glob
import subprocess
import re
import sys
import os
import time
from tqdm import tqdm
from modules.functions import update_progress, convert_time_to_seconds
from humanfriendly import parse_size


# These regular expressions are used to extract specific information from the output of a subprocess.
regex_duration = re.compile(
    r"Processing audio with duration (\d{2}(:\d{2}){0,2}\.\d{3})")
regex_time = re.compile(r"Processing segment at (\d{2}(:\d{2}){0,2}\.\d{3})")
regex_device_gpu = re.compile(r"GPU #(\d+): (.+)")
regex_device_cpu = re.compile(r"CPU: (.+)")
regex_download_model = re.compile(
    r"Downloading[^:]+:\s+\d+%\|[^|]+\|\s+(\d+\.\d+[A-Z]+)\/(\d+\.\d+[A-Z]+)")
# This is the regex pattern that matches the error message
regex_no_speech_threshold = re.compile(r"No speech threshold is met")


def run_subprocess(command):
    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding='utf-8'  # Use the 'utf-8' character map
    )


def get_file_info(process, file_name, config, file_count, files_to_transcribe):
    """
    The function `get_file_info` retrieves information about the file being processed, such as the
    device being used (CPU or GPU), the total duration of the file, and the current time of the
    transcription process.

    :param process: The `process` parameter is the subprocess that is running the command to get the
    file information. It is used to read the output of the command line by line
    :param file_name: The `file_name` parameter is the name of the file for which you want to get
    information
    :param config: The `config` parameter is a dictionary that contains various configuration settings
    for the file processing. It may include settings such as the device to be used (CPU or GPU), the
    file format, the output format, etc
    :return: the `progress_bar` object.
    """
    total_duration_var = None
    current_time = None
    device_name = None
    progress_bar = tqdm(total=100, position=0, leave=True, dynamic_ncols=True)
    close_progress_bar = False

    for line in process.stdout:
        # This line is for debugging purposes
        # print(line)

        if config['DEVICE'] == "cpu":
            # Match device CPU
            if match_device_cpu := regex_device_cpu.search(line):
                device_name = match_device_cpu.group(1)
                progress_bar.set_description(
                    f"Getting information about your CPU: {device_name}"
                )
        else:
            # Match device GPU
            if match_device_gpu := regex_device_gpu.search(line):
                device_name = match_device_gpu.group(2)
                progress_bar.set_description(
                    f"Getting information about your GPU: {device_name}"
                )

        # Match download model
        if match_download := regex_download_model.search(line):
            current_value = match_download.group(1)
            total_value = match_download.group(2)

            current_value_parsed = parse_size(current_value)
            current_value_parsed_mb = round(current_value_parsed / 1000000)
            total_value_parsed = parse_size(total_value)
            total_value_parsed_mb = round(total_value_parsed / 1000000)

            progress_bar.set_description(
                f"Downloading Model {config['MODEL']}:"
            )

            # Update progress bar
            update_progress(progress_bar, current_value_parsed_mb,
                            total_value_parsed_mb)

        # Match duration
        if match_duration := regex_duration.search(line):
            total_duration_var = convert_time_to_seconds(
                match_duration.group(1))
            progress_bar.set_description(
                f"Preparing Transcription using {device_name}:"
            )

        # Match time
        if match_current_time := regex_time.search(line):
            current_time = convert_time_to_seconds(
                match_current_time.group(1))
            progress_bar.set_description(
                f"Transcribing using {device_name}: File {file_name} ({file_count}/{files_to_transcribe})"
            )
            # Update progress bar
            update_progress(progress_bar, current_time, total_duration_var)

        # Match no speech threshold
        if match_speech_threshold := regex_no_speech_threshold.search(line):
            close_progress_bar = True

    # Update progress bar
    if (close_progress_bar):
        progress_bar.set_description(
            f"No speech detected, skipping file {file_name} ({file_count}/{files_to_transcribe})"
        )
        progress_bar.update(100 - progress_bar.n)

    return progress_bar


def handle_conversion_interrupted(process, progress_bar):
    """
    The above code defines functions to handle conversion interruption and errors, as well as a function
    to run a subprocess.

    :param process: The `process` parameter is an instance of the `subprocess.Popen` class. It
    represents a running subprocess and allows you to interact with it, such as terminating it or
    reading its output
    :param progress_bar: The `progress_bar` parameter is an object that represents a progress bar. It is
    used to display the progress of a conversion process
    """
    print("Conversion interrupted by user.")
    progress_bar.close()
    process.terminate()
    sys.exit(1)


def handle_error(e, process, progress_bar):
    print("An error occurred:", str(e))
    progress_bar.close()
    process.terminate()
    sys.exit(1)


def run_subprocess(command):
    return subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
    )


def transcription(config, wave_list, files_to_transcribe):
    """
    The function `transcription` transcribes a list of wave files using a specified configuration.

    :param config: A dictionary containing various configuration settings for the transcription process.
    It includes keys such as 'OUTPUT_DIR_NAME', 'OUTPUT_DIR_ACTIVATION', 'EXEFILE_GPU', 'DEVICE',
    'MODEL', 'CPU_THREADS', 'MODEL_DIR', 'LANGUAGE', 'COMPUTE_TYPE', 'OUT_FORMAT', and
    :param wave_list: The `wave_list` parameter is a list of tuples containing information about each
    wave file to be transcribed. Each tuple in the list contains three elements:
    """
    check_file = None
    file_count = 1

    for wavefile, current_folder, file_name in wave_list:
        whisper_folder = os.path.join(
            current_folder, config['OUTPUT_DIR_NAME'])
        if not os.path.exists(whisper_folder):
            os.makedirs(whisper_folder)

        if config['OUTPUT_DIR_ACTIVATION']:
            output_file_path = os.path.join(
                config['OUTPUT_DIR'])
            whisper_folder = output_file_path

        # Generating the output file name to check if the file already exists
        check_file = os.path.join(whisper_folder, file_name)

        # If the file does not exist, then run the transcription
        if not glob.glob(check_file + ".*"):
            command = [
                config['EXEFILE_GPU'],
                "--device", config['DEVICE'],
                "--model", config['MODEL'],
                "--threads", str(config['CPU_THREADS']),
                "--model_dir", config['MODEL_DIR'],
                "--output_dir", whisper_folder,
                "--language", config['LANGUAGE'],
                "--compute_type", config['COMPUTE_TYPE'],
                "--output_format", config['OUT_FORMAT'],
                "--verbose", "true",
                wavefile
            ]
            # Add the VAD filter if it is enabled
            if config['VAD_FILTER']:
                command.append("--vad_filter")
                command.append("true")

            # Add the BEEP flag if it is enabled
            if not config['BEEP_SOUND']:
                command.append("--beep_off")

            # Run the transcription
            process = run_subprocess(command)
            progress_bar = get_file_info(
                process, file_name, config, file_count, files_to_transcribe)
            # Add file counter to the list of files to transcribe
            file_count += 1

            try:
                try:
                    # Placeholder for potentially additional code
                    pass
                except KeyboardInterrupt:
                    handle_conversion_interrupted(
                        process, progress_bar)

                process.wait()
                process.terminate()

                progress_bar.set_postfix(
                    {"Transcription is complete": "100%"})
                progress_bar.n = progress_bar.total  # Set the progress value to the total
                progress_bar.refresh()  # Re

                progress_bar.close()
            except Exception as e:
                handle_error(e, process, progress_bar)
    else:
        print("No more sound files to transcribe.")
