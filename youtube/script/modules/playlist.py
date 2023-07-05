import os
import subprocess
import sys
import time
from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from modules.cookie import CookieUtils
from modules.functions import is_text_file_empty, check_lowest_expiry
import requests


class GeneratePlayList(Process):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        cookie_utils = CookieUtils()
        generate_cookie_flag = False
        run_command = None

        if self.config['useAuthCookie'] == "true":
            if is_text_file_empty(self.config['cookieTimerPath']):
                generate_cookie_flag = True
            elif check_lowest_expiry(self.config['cookieTimerPath']):
                generate_cookie_flag = True
                print(
                    "Cookie is expired, yu need either to login or generate a new cookie")
            else:
                run_command = True

        if (generate_cookie_flag):
            # We need to generate the cookie file
            generate_cookie = cookie_utils.generate_cookie_file(
                self.config['baseSite'],
                self.config['browser'],
                self.config['chromeProfileLocation'],
                self.config['chromeExeLocation'],
                self.config['authCookie'],
                self.config['cookieTimerPath'])

            if (generate_cookie):
                print("Cookie generated successfully")
                run_command = True
            else:
                print("Failed to generate cookie")

        if (run_command):
            print("Running command")

    def run_subprocess(command):
        """
        The function `run_subprocess` runs a command as a subprocess and returns the output.

        :param command: The `command` parameter is a string that represents the command you want to run in
        the subprocess. It can be any valid command that you would normally run in a terminal or command
        prompt
        :return: a subprocess.Popen object.
        """
        return subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
        )
