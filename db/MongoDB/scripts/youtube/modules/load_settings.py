# Calculate the absolute path of the configuration file
import os
from pathlib import Path

import yaml


def get_config():
    load_yaml = os.path.join(os.path.dirname(
        Path(__file__).resolve()), '../settings.yaml')

    # Read the YAML file
    with open(load_yaml, "r") as file:
        config = yaml.safe_load(file)

    return config
