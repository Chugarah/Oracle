import json
import os


def read_settings():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(script_directory)
    file_path = os.path.join(
        parent_directory, 'youtube-conf', 'youtube-settings.json')

    with open(file_path, 'r') as f:
        settings = json.load(f)

    return settings
