
import os
from pathlib import Path
from dotenv import load_dotenv
from modules.worker_whisper import Worker_whisper
import yaml

# Calculate the absolute path of the configuration file
load_yaml = os.path.join(os.path.dirname(
    Path(__file__).resolve()), 'settings.yaml')

# Read the YAML file
with open(load_yaml, "r") as file:
    config = yaml.safe_load(file)

# Create a single instance of Worker_ffmpeg and start the thread
Worker_whisper = Worker_whisper(config)
Worker_whisper.start()
# Wait for the Worker_ffmpeg thread to finish
Worker_whisper.join()
