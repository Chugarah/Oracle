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

### 4. Update Yt-dlp

This step is optional. If you want to update yt-dlp to the latest version, run the following command:

```powershell
.\youtube\script\yt-dlp.exe -U
```

### 5. Edit some configuration files

We need to set path from where where we want to store the files and where we should convert it from using FFmpeg. We need to edit the following files: They are inside youtube-conf folder

1. youtube-links.json. Just add the links as example bellow and save the file.

    ```json
    [
        {
        "URL": "https://www.youtube.com/watch?v=LXb3EKWsInQ"
        },
        {
        "URL": "https://www.youtube.com/shorts/GbcVJEuOjqc"
        }
    ]
    ```

2. youtube-settings.json. The "inputFolder" is where the FFmpeg will look for files to convert. The rest does not need editing

    ```json
    {
        "config": "youtube/script/youtube-conf/yt-dlp.conf",
        "inputFolder": "youtube/files/",  // is where the FFmpeg will look for sound files to convert
        "jsonFile": "youtube/script/youtube-conf/youtube-links.json"
    }
    ```

3. yt-dlp.conf. This is the main conf file for yt-dlp. More detail information can be found <https://github.com/yt-dlp/yt-dlp#general-options>. This settings that I provided in this modules, download the best quality video and audio and then merge them together. It also download the best audio quality.The rest does not need editing. If you want to test or satisfied with current settings the only line needs editing is where you place the path to the folder where you want to store the files.

    This is also how the files will be organized. The example bellow will save the files in the folder youtube/files/ and then it will create a folder for each channel, year, month and then id of the video. The file will be named as id of the video. The file extension will be the same as the original file. The example bellow will save the file as youtube/files/channel_id/year/month/id/id.extension

    Remember we are running from root directory (oracle). So it will save the files in oracle/youtube/files/

    The lines we are interested in editing is:

    ```config
    # Save all videos under specified directory with structured organization by channel, year, month, and id
    -o youtube/files/%(channel_id)s/%(upload_date>%Y)s/%(upload_date>%m)s/%(id)s/%(id)s.%(ext)s
    
    # Disable this by putting an # in front of the line
    --write-comments

    # Set rate limit to 10 MB/s, change this to whatever you want
    --limit-rate 10000K
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
    "config": "youtube/script/youtube-conf/yt-dlp.conf",
    "inputFolder": "youtube/files/",
    "jsonFile": "youtube/script/youtube-conf/youtube-links.json",
    "cookieAuth": true  // <<---- Thus one
}
```

If you want to manually create the cookie file, you can do it downloading an google chrome extension called EditThisCookie <https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg/related>

Copy later the values into this website <https://www.cookieconverter.com/> but place your text at the bottom and the result will be display on top "Netscape". Copy that text and paste it in the file "youtube/script/youtube-conf/auth_cookie.txt". I have not tried this option yet, but it should work. The important note that the format of auth_cookie.txt file should be Netscape cookie format.

### 8. Final Step, run the script

We are running the script from root directory (oracle).

```powershell
python .\youtube\script\main.py
```
