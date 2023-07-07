import json
import os
import re

import sys
import time
from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import requests
from urllib.parse import urlparse, parse_qs
from modules.playlist_core import PlayListCore


class GeneratePlayList(Process):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        PlayListCore.play_list_init(self.config)
