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
    def __init__(self, link, config, total_links, file_counter):
        super().__init__()
        self.link = link
        self.config = config
        self.total_links = total_links
        self.file_counter = file_counter

    def run(self):

        video_id = extract_video_id(self.link)
        result = FolderScanner.scan_folder(
            self.config['inputFolder'], ['.webm', '.mp4'])

        if not any(video_id == item[2] for item in result):
             download_video(self.link, self.config, video_id,
                          self.total_links, self.file_counter)
        return
