import json
import os
import re
import subprocess
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
from modules.cookie import CookieUtils
from modules.functions import is_text_file_empty, check_lowest_expiry
import requests
from urllib.parse import urlparse, parse_qs

# Regex to get the data
playlist_name_regex = re.compile(r'\[download\] Downloading playlist: (.*)')
total_links_regex = re.compile(r'Downloading \d+ items of (\d+)')
current_link_regex = re.compile(r'Downloading item (\d+) of \d+')


class GeneratePlayList(Process):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        cookie_utils = CookieUtils()
        generate_cookie_flag = False
        run_command = None
        user_use_cookie = False
        if self.config['useAuthCookie'] == "true":
            user_use_cookie = True
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
            command = [
                "youtube/script/yt-dlp.exe",
                "--get-url",
                "--flat-playlist",
                "--verbose",
                "--skip-download",
                "--no-warnings",
                "https://www.youtube.com/watch?v=YZ5tOe7y9x4&list=PL4PUlDYnSnDDfcMwPKLNLliqo76lclyt5"
            ]

            # Add the Cookie if user enables authentication
            if user_use_cookie:
                command.append("--cookies")
                command.append(self.config['authCookie'])

            self.get_file_info(command)

            input_file = self.config['playListVideoRaw']
            output_file = self.config['videoLinks']
            self.extract_video_ids(input_file, output_file)

    def extract_video_ids(self, input_file, output_file):
        # Delete the output file if it exists
        if os.path.exists(output_file):
            os.remove(output_file)

        # Recreate the output file if it doesn't exist
        if not os.path.exists(output_file):
            with open(output_file, 'w') as file:
                pass

        with open(input_file, 'r') as file:
            lines = file.readlines()

            video_info = []

            for i in range(len(lines)):
                if lines[i].startswith("[download] Downloading item"):
                    video_id = lines[i].split()[-1]
                    url = lines[i+1].strip()
                    if url:  # Exclude empty URLs
                        video_info.append(f"{url.strip()}\n")

            with open(output_file, 'w') as output:
                output.writelines(video_info)

    def get_file_info(self, command):
        play_list_name = None
        play_list_total_items = 0
        play_list_current_item = 0
        file_name = "youtube-links.json"
        progress_bar = tqdm(total=100, position=0,
                            leave=True, dynamic_ncols=True)
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
        )

        with open(self.config['playListVideoRaw'], "w") as subprocess_stdout:
            while True:
                line = process.stdout.readline()
                if not line:
                    break

                line = line.strip()
                # print(line)

                # Getting the playlist name
                if match_playlist_name := playlist_name_regex.search(line):
                    play_list_name = match_playlist_name.group(1)

                # Getting the total items in the playlist
                if match_items := total_links_regex.search(line):
                    play_list_total_items = match_items.group(1)
                    progress_bar.set_description(
                        f"Preparing to items {play_list_name} playlist: {play_list_current_item} / {play_list_total_items} items"
                    )

                # Getting the current item name
                if match_playlist_current_value := current_link_regex.search(line):
                    play_list_current_link = match_playlist_current_value.group(
                        1)

                    # Convert the strings to integers
                    play_list_current_link = int(play_list_current_link)
                    play_list_total_items = int(play_list_total_items)

                    # If current_value is greater than total duration,
                    # set progress bar to 100%
                    if play_list_current_link > play_list_total_items:
                        progress_bar.update(100 - progress_bar.n)
                    else:
                        progress_bar.set_description(
                            f"Preparing to items {play_list_name} playlist: {play_list_current_link} / {play_list_total_items} items"
                        )

                        # Calculate the progress percentage
                        progress_percentage = (
                            play_list_current_link / play_list_total_items
                        ) * 100
                        # Round the progress percentage to two decimal places
                        rounded_progress_percentage = round(
                            progress_percentage, 0)
                        # Update the progress bar
                        progress_bar.update(
                            rounded_progress_percentage - progress_bar.n
                        )

                subprocess_stdout.write(line + "\n")

        process.wait()
        progress_bar.refresh()

    def run_subprocess(self, command):
        """
        The function `run_subprocess` runs a command as a subprocess and returns the output.

        :param command: The `command` parameter is a string that represents the command you want to run in
        the subprocess. It can be any valid command that you would normally run in a terminal or command
        prompt
        :return: a tuple containing the output and the error (output, error)
        """
        with subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
        ) as process:
            output, error = process.communicate()
        return output, error
