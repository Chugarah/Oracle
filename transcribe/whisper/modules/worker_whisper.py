from collections import Counter
import os
from pathlib import Path
import threading


from modules.transcribe import transcription
output_lock = threading.Lock()
debug = False


# The `Worker_whisper` class is a subclass of `threading.Thread` that scans a folder for MP3 files,
# normalizes their paths, and then passes the list of files to a `transcription` function.
class Worker_whisper(threading.Thread):

    def __init__(self, config):

        super().__init__()
        self.config = config

    def run(self):

        def scan_folder(folder):
            wave_list = []
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith(".mp3"):
                        webm_path = os.path.join(root, file)
                        normalized_path = os.path.normpath(webm_path)
                        current_folder = os.path.dirname(normalized_path)
                        file_name_without_extension = os.path.splitext(os.path.basename(normalized_path))[
                            0]
                        wave_list.append(
                            (normalized_path, current_folder, file_name_without_extension))
            return wave_list

        wave_list = scan_folder(
            self.config['INPUT_DIR'])

        print(len(wave_list))

        if (len(wave_list) <= 0):
            print("No wav files found in the input directory to transcribe.")
        else:
            transcription(self.config, wave_list)
