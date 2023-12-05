# Module : Youtube Downloader

Welcome traveler, to the youtube downloader module. This module is using yt-dlp to download youtube videos. The module is using Python and Conda. The step of the module is to get it to work in Windows and then Linux. Now supporting Windows environments only

Lets start with system requirements.

## System Requirements

* Conda <https://docs.conda.io/en/latest/miniconda.html>
* PowerShell <https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.3>
* Windows 10+
* Git <https://git-scm.com/download/win> (We are using Conda to Install Git)
* FFmpeg <https://ffmpeg.org/download.html> (We are using Conda to Install FFmpeg)

## Installation - Clone Repo

Lets start by cloning the repo. Open PowerShell and type the following command:

### 1. Clone Repo

```powershell
git clone https://github.com/Chugarah/Oracle.git
cd oracle
```

### 2. Create Conda Environment

This assumes that you have made the base environment. If not, please read the on the root page README.md file.

```powershell
conda install -c conda-forge ffmpeg
```

### 3. Install Python Packages

```powershell
pip install -r .\youtube\script\requirements.txt
```

### 4. Update Yt-dlp (Optional) &  Conda Packages

This step is optional. If you want to update yt-dlp to the latest. version, run the following command:

```powershell
.\youtube\script\yt-dlp.exe -U
conda update --all
conda install -c conda-forge --update-deps webdriver-manager
```

### 5. Edit some configuration files

We need to set path from where where we want to store the files and where we should convert it from using FFmpeg. We need to edit the following files: They are inside youtube-conf folder

1. video_links.txt. This file is where you put your youtube links or playlist. Look at the example below. The example below is 10 videos from The Kiffness <https://www.youtube.com/channel/UCFy846QdKs3LbLgBpSqPcdg>

    ```txt
    https://www.youtube.com/watch?v=JjBRlnO6LvA&list=PLqWxGh_2yxf_xCKNnYXfGpD10EBEv7p2Y
    https://www.youtube.com/watch?v=2DRSEQ5JBic
    ```

2. youtube-settings.json. The "inputFolder" is where the FFmpeg will look for files to convert. The rest does not need editing

    ```json
    {
        "authentication": "false",
        "config": "youtube/script/youtube-conf/yt-dlp.conf",
        "browser": "chrome",
        "videoLinks": "youtube/script/youtube-conf/video_links.txt",
        "playListVideoRaw": "youtube/script/youtube-conf/playlist-links-parser.txt",
        "linkReader": "youtube/script/youtube-conf/link-reader.txt",
        "inputFolder": "youtube/files/",
        "authCookie": "youtube/script/youtube-conf/auth/auth_cookie.txt",
        "cookieTimerPath": "youtube/script/youtube-conf/auth/cookie_timer.txt",
        "chromeProfileLocation": "C:/Users/User/AppData/Local/Google/Chrome/User Data",
        "chromeExeLocation": "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "baseSite": "https://www.youtube.com"
    }
    ```

    Detail explanation of each line:

    | Key                   | Description                                                                                                                                                                                                                          |
    | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | authentication        | Enable this to use Cookie authentication                                                                                                                                                                                             |
    | config                | The configuration file for yt-dlp.exe location                                                                                                                                                                                       |
    | browser               | Which browser to open for to refresh our cookie authentication. Oracle supports Chrome only for the moment                                                                                                                           |
    | videoLinks            | This is the file you add your video links or playlist links.                                                                                                                                                                         |
    | playListVideoRaw      | This is file where the raw output from our yt-dlp.exe is being parsed from. This file should not be edited                                                                                                                           |
    | linkReader            | This file is the same as playListVideoRaw, just an file to be parsed. Should not be edited                                                                                                                                           |
    | inputFolder           | This is the folder where FFmpeg will look and also our location where we store our youtube content                                                                                                                                   |
    | authCookie            | Place where your cookie data will be stored, please don't edit this                                                                                                                                                                  |
    | cookieTimerPath       | Place where the cookie timer will be stored, please don't edit this                                                                                                                                                                  |
    | chromeProfileLocation | This is the location of your chrome profile. This is used to get the cookie data. This is default storage for default user and for windows. Based if you have multiple profiles you need to change this to the profile you are using |
    | chromeExeLocation     | This is the location of your chrome.exe. This is used to open chrome to refresh the cookie. That is the default location if you don't install it in custom location. data                                                            |
    | baseSite              | This is the base site for youtube. I use .com but can be anything based on your preference but it need to be youtube. this                                                                                                           | ' |

    The line is that good to start is "inputFolder". This is where you place the path to the folder where you want to store the files. The rest does not need editing. If you want to test or satisfied with current settings the only line needs editing is where you place the path to the folder where you want to store the files.

3. yt-dlp.conf. This is the main conf file for yt-dlp. More detail information can be found <https://github.com/yt-dlp/yt-dlp#general-options>. This settings that I provided in this modules, download the best quality video and audio and then merge them together. It also download the best audio quality.The rest does not need editing. If you want to test or satisfied with current settings the only line needs editing is where you place the path to the folder where you want to store the files.

    This is also how the files will be organized. The example bellow will save the files in the folder youtube/files/ and then it will create a folder for each channel, year, month and then id of the video. The file will be named as id of the video. The file extension will be the same as the original file. The example bellow will save the file as youtube/files/channel_id/year/month/id/id.extension

    Remember we are running from root directory (oracle). So it will save the files in oracle/youtube/files/

    The lines we are interested in editing is:

    ```config

    # This is a complete guess, but I think YTDLP pretends to be a normal web browser fetching videos from YouTube' servers. 
    # As such, YT would have no reason to stop lots of downloads from YTDLP as much as it would stop someone from playing 40 
    # chrome tabs of YouTube videos all at once.

    # Download the highest video resolution and best audio quality in separate formats and then merge them. You can change this to your liking. 
    # And also download the best audio separately.
    -f "bestvideo+bestaudio/best,bestaudio"

    # Save all videos under specified directory with structured organization by channel, year, month, and id
    -o youtube/files/%(channel_id)s/%(upload_date>%Y)s/%(upload_date>%m)s/%(id)s/%(id)s.%(ext)s

    # Download English subtitles, descriptions, comments, thumbnails, links, etc.
    --sub-lang en
    --write-auto-subs
    --write-description
    --write-info-json
    --write-comments
    --write-thumbnail
    --write-link
    --embed-thumbnail
    --embed-metadata
    --embed-chapters
    --embed-info-json

    # Maintain rate limiting as before
    --min-sleep-interval 5
    --max-sleep-interval 15

    # Include progress in output, please don't touch this, this is to update the progress bar
    --progress

    # Set rate limit to 0.5 MB/s, change this to whatever you want
    --limit-rate 25000K

    # Use local proxy, this is optional, but recommended for better performance
    --proxy 127.0.0.1:8118

    ```

### 6. Install Proxy Server

The yt-dlp community recommend an proxy server for better performance. I am using Privoxy for Windows. <http://www.privoxy.org/>. Download and install it, after the installation you have to edit the "yt-dlp.conf" file in youtube and add the line below. The port number is the default port number for Privoxy.

```powershell
# Use local proxy
--proxy 127.0.0.1:8118
```

### 8. Authentication for Youtube

This step is optional. If you want to download private videos, you need to authenticate. The authentication is done by cookies. We will use Chrome with default user profile. Its important that you start your Chrome browser and login to youtube. If you are logged in, you can continue with the next step. This is only supported for Windows and Chrome browser.

The script is using selenium to get the cookies from Chrome. The script will look for the default user profile. If you have multiple user profiles, you have to change the default user profile to the one you want to use.

To enable Cookie auth function you have to edit the file "youtube-settings.json" and change the value of "cookieAuth" to true. The rest does not need editing. By default is off

```json
{
    "authentication": "false", <---- Change this to true to enable to activate authentication
    "config": "youtube/script/youtube-conf/yt-dlp.conf",
    "browser": "chrome",
    "videoLinks": "youtube/script/youtube-conf/video_links.txt",
    "playListVideoRaw": "youtube/script/youtube-conf/playlist-links-parser.txt",
    "linkReader": "youtube/script/youtube-conf/link-reader.txt",
    "inputFolder": "youtube/files/",
    "authCookie": "youtube/script/youtube-conf/auth/auth_cookie.txt",
    "cookieTimerPath": "youtube/script/youtube-conf/auth/cookie_timer.txt",
    "chromeProfileLocation": "C:/Users/User/AppData/Local/Google/Chrome/User Data",
    "chromeExeLocation": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "baseSite": "https://www.youtube.com"
}
```

If you want to manually create the cookie file, you can do it downloading an google chrome extension called EditThisCookie <https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg/related>

Copy later the values into this website <https://www.cookieconverter.com/> but place your text at the bottom and the result will be display on top "Netscape". Copy that text and paste it in the file "youtube/script/youtube-conf/auth_cookie.txt". I have not tried this option yet, but it should work. The important note that the format of auth_cookie.txt file should be Netscape cookie format.

### 8. Final Step, run the script

We are running the script from root directory (oracle).

```powershell
python .\youtube\script\main.py
```
