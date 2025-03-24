import re
import sys
import os
import time
from tqdm import tqdm
from ffmpeg import FFmpeg, Progress
from modules.functions import update_progress, convert_time_to_seconds

regex_duration = re.compile(r"Duration: (\d{2}:\d{2}:\d{2}\.\d{2})")
regex_time = re.compile(r"time=(\d{1,2}:\d{1,2}:\d{1,2}\.\d{2})")
get_extension = re.compile(r"#0, (.*?), to")


def handle_conversion_interrupted(progress_bar, output_file, ffmpeg_instance=None):
    print("Conversion interrupted by user.")
    progress_bar.close()

    if ffmpeg_instance:
        ffmpeg_instance.terminate()

    if os.path.exists(output_file):
        os.remove(output_file)
    sys.exit(1)


def handle_error(e, progress_bar, output_file, ffmpeg_instance=None):
    print("An error occurred:", str(e))
    progress_bar.close()

    if ffmpeg_instance:
        ffmpeg_instance.terminate()

    if os.path.exists(output_file):
        time.sleep(5)
        os.remove(output_file)
    sys.exit(1)


def convert_sound(webm_files, output_file, file_khz, file_name, files_to_convert, file_counter):
    progress_bar = tqdm(total=100, position=0, leave=True, dynamic_ncols=True)
    progress_bar.set_description(
        f"Converting file {file_counter} / {files_to_convert}: {file_name}")

    # Create FFmpeg instance
    ffmpeg = (
        FFmpeg()
        .option("y")  # Overwrite output files without asking
        .input(webm_files)
        .output(
            output_file,
            {
                "vn": None,              # No video
                "acodec": "libmp3lame",  # MP3 codec
                "b:a": "320k",           # Bitrate
                "ac": "2",               # 2 Audio channels (stereo)
                "ar": file_khz,          # Sample rate
                "map_metadata": "0",     # Copy metadata
                "id3v2_version": "3"     # ID3 version
            }
        )
    )

    # Set up progress handling
    total_duration = None

    @ffmpeg.on("stderr")
    def on_stderr(line):
        nonlocal total_duration

        # Extract duration if not already set
        if total_duration is None:
            if match := regex_duration.search(line):
                total_duration = convert_time_to_seconds(match.group(1))

        # Update progress based on time
        if match := regex_time.search(line):
            current_value = round(convert_time_to_seconds(match.group(1)), 3)

            if total_duration:
                # If current_value is greater than total duration,
                # set progress bar to 100%
                if current_value > total_duration:
                    progress_bar.update(100 - progress_bar.n)
                else:
                    progress_bar.update(
                        (current_value/total_duration)*100 - progress_bar.n)

                progress_bar.refresh()

    @ffmpeg.on("progress")
    def on_progress(progress: Progress):
        # This is an alternative way to track progress if the stderr method doesn't work reliably
        if total_duration and progress.time and progress.time > 0:
            percent = min(100, (progress.time / total_duration) * 100)
            progress_bar.update(percent - progress_bar.n)
            progress_bar.refresh()

    try:
        try:
            # Execute FFmpeg
            ffmpeg.execute()
        except KeyboardInterrupt:
            handle_conversion_interrupted(progress_bar, output_file, ffmpeg)

        progress_bar.close()
    except Exception as e:
        handle_error(e, progress_bar, output_file, ffmpeg)
