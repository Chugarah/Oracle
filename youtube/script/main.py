import json
import os
from tqdm import tqdm
from pathlib import Path
import subprocess

from modules.worker import Worker
from modules.worker_ffmpeg import Worker_ffmpeg
from modules.settings import read_settings

# Read Config file
config, input_folder, json_file = read_settings()

# file_path = os.path.join(os.path.dirname(
with open(json_file, 'r') as f:
    youtube_links = json.load(f)

# The code is iterating over a list of YouTube links stored in the `youtube_links` variable. For each
# link, it creates a `Worker` object with the link as a parameter. The `Worker` object is responsible
# for performing some task related to the YouTube link.
workers = []
for link in youtube_links:
    # Create a Worker object for the current link
    worker = Worker(link)
    # Start the Worker thread
    worker.start()
    workers.append(worker)

# Wait for all the Worker threads to finish
for worker in workers:
    worker.join()

# Create a single instance of Worker_ffmpeg and start the thread
worker_ffmpeg = Worker_ffmpeg()
worker_ffmpeg.start()
# Wait for the Worker_ffmpeg thread to finish
worker_ffmpeg.join()
