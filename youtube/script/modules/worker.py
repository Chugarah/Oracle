import os
import random
import time
from pathlib import Path
import threading
from tqdm import tqdm

from modules.settings import read_settings
from modules.downloader import download_video
from modules.file_handler import FolderScanner
from modules.functions import extract_video_id

# The Worker class is a subclass of threading.Thread that downloads a video if its ID is not found in
# a list of scanned files.


class Worker(threading.Thread):
    def __init__(self, link):
        super().__init__()
        self.link = link

    def run(self):

        video_url = self.link['URL']
        video_id = extract_video_id(video_url)

        config, input_folder, json_file = read_settings()

        result = FolderScanner.scan_folder(input_folder, ['.webm', '.mp4'])

        if not any(video_id == item[2] for item in result):
            download_video(video_url, config, video_id)
            return
