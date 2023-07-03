import json
import os
import chardet


def read_settings():

    # Get the directory of the Python script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(
        script_directory)  # Get the parent directory
    file_path = os.path.join(
        parent_directory, 'youtube-conf', 'youtube-settings.json')

    with open(file_path, 'r') as f:
        settings = json.load(f)

    return settings['config'], settings['inputFolder'], settings['jsonFile']
