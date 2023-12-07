from asyncio import sleep
import os
import re
import subprocess
from modules.cookie import CookieUtils
from tqdm import tqdm
from modules.functions import is_text_file_empty, check_lowest_expiry, run_subprocess, create_file_if_not_exists

# Regex to get the data
playlist_name_regex = re.compile(r'\[download\] Downloading playlist: (.*)')
total_links_regex = re.compile(r'Downloading \d+ items of (\d+)')
current_link_regex = re.compile(r'Downloading item (\d+) of \d+')
video_info = set()


class PlayListCore:

    @staticmethod
    def play_list_init(config):
        """
        The `play_list_init` function initializes a playlist by generating a cookie file if necessary, and
        then retrieves video URLs from the playlist and saves them to a file.

        :param config: A dictionary containing various configuration settings for the playlist
        initialization process. The dictionary should have the following keys:
        """
        cookie_utils = CookieUtils()
        generate_cookie_flag = False
        run_command = None
        user_use_cookie = False

        if config['authentication'] == "true":

            # Lets create the cookie files if it does not exists
            create_file_if_not_exists(config['authCookie'])
            create_file_if_not_exists(config['cookieTimerPath'])

            user_use_cookie = True
            if is_text_file_empty(config['cookieTimerPath']):
                generate_cookie_flag = True
            elif check_lowest_expiry(config['cookieTimerPath']):
                generate_cookie_flag = True
                print(
                    "Cookie is expired, yuo need either to login or generate a new cookie")
            else:
                run_command = True

            if (generate_cookie_flag):
                # We need to generate the cookie file
                generate_cookie = cookie_utils.generate_cookie_file(
                    config['baseSite'],
                    config['browser'],
                    config['chromeProfileLocation'],
                    config['chromeExeLocation'],
                    config['authCookie'],
                    config['cookieTimerPath'])

                if (generate_cookie):
                    print("Cookie generated successfully")
                    run_command = True
                else:
                    print("Failed to generate cookie")
        else:
            # We till need to run the command even if authentication is false
            run_command = True

        if (run_command):

            # We need to insert for each playlist the url
            # Lets delete delete the link reader
            input_file = config['playListVideoRaw']
            output_file = config['linkReader']

            # Lets enable the progress bar
            progress_bar = tqdm(total=100, position=0,
                                leave=True, dynamic_ncols=True)

            PlayListCore.extract_video_ids(
                mode="delete", output_file=output_file)
            try:
                with open(config['videoLinks'], 'r') as file:
                    lines = file.readlines()
                    if len(lines) == 0:
                        progress_bar.set_description(
                            f"Playlist is empty, please add videos to the playlist"
                        )
                        progress_bar.update(100 - progress_bar.n)
                    else:
                        for line in lines:
                            command = [
                                "youtube/script/yt-dlp.exe",
                                "--get-url",
                                "--flat-playlist",
                                "--verbose",
                                "--skip-download",
                                "--no-warnings",
                                line
                            ]

                            # Add the Cookie if user enables authentication
                            if user_use_cookie:
                                command.append("--cookies")
                                command.append(config['authCookie'])

                            # Get the output and error from the subprocess, also display an progress bar
                            PlayListCore.get_file_info(
                                command, config, progress_bar)

                            PlayListCore.extract_video_ids(
                                input_file, output_file)

            except FileNotFoundError:
                print("The file does not exist.")

    @staticmethod
    def get_file_info(command, config, progress_bar):
        """
        The `get_file_info` function reads the output of a subprocess command line by line, extracts
        information such as playlist name, total items, and current item, and updates a progress bar
        accordingly.

        :param command: The `command` parameter is a string that represents the command to be executed in
        the subprocess. It is passed to the `subprocess.Popen` function to start the subprocess and capture
        its output
        :param config: The `config` parameter is a dictionary that contains various configuration settings
        for the function. It is used to specify the file paths and other options required for the function
        to work correctly. The specific keys and their corresponding values in the `config` dictionary are
        not provided in the code snippet, so it is
        """
        play_list_name = None
        play_list_total_items = 0
        play_list_current_item = 0
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
        )

        with open(config['playListVideoRaw'], "w") as subprocess_stdout:
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                # For Debugging purposes
                # print(line)

                # Getting the playlist name
                if match_playlist_name := playlist_name_regex.search(line):
                    play_list_name = match_playlist_name.group(1)

                # Getting the total items in the playlist
                if match_items := total_links_regex.search(line):
                    play_list_total_items = match_items.group(1)
                    progress_bar.set_description(
                        f"Processing items {play_list_name} playlist: {play_list_current_item} / {play_list_total_items} items"
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
                            f"Processing items {play_list_name} playlist: {play_list_current_link} / {play_list_total_items} items"
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

    @staticmethod
    def extract_video_ids(input_file=None, output_file=None, mode=None):
        """
        The function `extract_video_ids` extracts YouTube video IDs from an input file and writes them to an
        output file, with an option to delete the output file before running.

        :param input_file: The input_file parameter is the path to the file from which you want to extract
        video IDs
        :param output_file: The output_file parameter is the name or path of the file where the extracted
        video IDs will be written
        :param mode: The "mode" parameter determines the behavior of the function. If the mode is set to
        "delete", the function will delete the output file if it exists and recreate it. If the mode is set
        to any other value, the function will read the input file, extract video URLs from it, and
        """

        # We need to call this before, because we need to delete the file
        if (mode == "delete"):
            # Delete the output file if it exists
            if os.path.exists(output_file):
                os.remove(output_file)

            # Recreate the output file if it doesn't exist
            if not os.path.exists(output_file):
                with open(output_file, 'w') as file:
                    pass
        else:
            # This pattern matches lines that only contain a YouTube URL
            url_only_pattern = r"^(https://www\.youtube\.com/watch\?v=[^\n&]+)$"

            # This pattern matches lines starting with "[youtube] Extracting URL: "
            youtube_extract_pattern = r"^\[youtube\] Extracting URL: (https://www\.youtube\.com/(?:watch\?v=|shorts/)[^\n&]+)"

            with open(input_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if "[youtube] Extracting URL: " in line:
                        match = re.search(youtube_extract_pattern, line)
                        if match:
                            video_url = match.group(1)
                            video_info.add(f"{video_url}\n")
                    else:
                        match = re.search(url_only_pattern, line.strip())
                        if match:
                            # Whole match is the URL, hence use group(0)
                            video_url = match.group(0)
                            video_info.add(f"{video_url}\n")

            with open(output_file, 'w') as output:
                output.writelines(video_info)
