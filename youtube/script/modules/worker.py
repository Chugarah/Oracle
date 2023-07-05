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

        print("Worker started")
