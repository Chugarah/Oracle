from collections import Counter
import os
from pathlib import Path
import shutil
import threading
import wave
from tqdm import tqdm

from modules.settings import read_settings
from modules.ffmpeg_conversion_worker import convert_sound

output_lock = threading.Lock()


class Worker_ffmpeg(threading.Thread):
    def __init__(self):
        super().__init__()

    def convert_to_seconds(time_string):
        # Convert time string in format HH:MM:SS.ss to seconds
        hours, minutes, seconds = time_string.split(':')
        seconds, milliseconds = seconds.split('.')
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + \
            int(seconds) + int(milliseconds) / 100
        return total_seconds

    def run(self):
        # Move this line above existing_files
        settings = read_settings()
        totalFiles = 0

        def scan_folder(folder):
            nonlocal totalFiles  # Declare totalFiles as non-local
            webm_files = []
            m4a_files = []
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith(".webm"):
                        webm_path = os.path.join(root, file)
                        normalized_path = os.path.normpath(webm_path)
                        webm_files.append(normalized_path)
                    elif file.endswith(".m4a"):
                        m4a_path = os.path.join(root, file)
                        normalized_path = os.path.normpath(m4a_path)
                        m4a_files.append(normalized_path)
            combined_files = webm_files + m4a_files
            totalFiles = len(combined_files)
            return combined_files, totalFiles

        combined_files, totalFiles = scan_folder(
            settings['inputFolder'])  # Assign the returned values

        mp3_count = len(list(Path(settings['inputFolder']).rglob("*.mp3")))

        totalFiles = len(combined_files)
        files_to_convert = totalFiles - mp3_count

        file_counter = 0

        for files in combined_files:
            # GPU Version
            mp3_file = os.path.splitext(files)[0] + ".mp3"
            mp3_file_name = os.path.basename(mp3_file)

            if not os.path.exists(mp3_file):
                file_counter += 1
                convert_sound(files, mp3_file, "48000",
                              mp3_file_name, files_to_convert, file_counter)

        if files_to_convert == 0:
            progress_bar = tqdm(total=100, position=0,
                                leave=True, dynamic_ncols=True)
            progress_bar.total = 100
            progress_bar.update(100)  # Update the progress to 100
            progress_bar.set_description("No Files to Convert")
            # Close the progress bar
            progress_bar.close()
