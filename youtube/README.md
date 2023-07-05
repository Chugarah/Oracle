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

This step is optional. If you want to download private videos, you need to authenticate. The authentication is done by cookies. The simple way to do this to extract the cookies from your youtube session using an browser extension called "EditThisCookie". You can download that extension here <https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg/related>.

#### 8.1 Extract Cookies

Download the extension, they are plenty of extension that does what "EditThisCookie" but for this example I selected that extension.

* Chrome/Edge: <https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg/related>

* Firefox <https://addons.mozilla.org/en-US/firefox/addon/edithiscookie/>

Some general guide on how to use the extension:
<https://www.youtube.com/watch?v=BnlcPvYAGVA>

When extension is installed, go to youtube.com and check that you are logged in. If you are logged in start the extension and find the button says "Export Cookies".

#### 8.2 Extract Cookies

Now we have to navigate to the folder where the cookies will be stored. The cookies are stored in the folder "youtube/script/youtube-conf/auth/browser_cookie.txt". Open the text file "browser_cookie.txt" and paste in the cookies. Save the file.

It looks something like this:

```text
{
    "domain": ".youtube.com",
    "expirationDate": 1721038123.786763,
    "hostOnly": false,
    "httpOnly": false,
    "name": "__Secure-3PAPISID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "opjew98rh389rhfheuwhior384example",
    "id": 1
},
```

It will be multiple lines of this, this is small part of the file. Please remember  that that this cookie will expire in 7 days and you need to redo this step 8.1 and 8.2.

### 8. Final Step, run the script

We are running the script from root directory (oracle).

```powershell
python .\youtube\script\main.py
```
