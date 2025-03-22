# Module : Media Downloader

Welcome traveler, to the media downloader module. This module is using yt-dlp to download videos from YouTube and other platforms. The module is using Python and can run both locally or via Docker. Previously it supported Windows environments only, but now it supports both Windows and Linux via Docker.

## Recent Updates

- **Improved Progress Tracking**: Now using yt-dlp's built-in progress hooks for more accurate download progress reporting
- **API-Based Integration**: Enhanced integration with yt-dlp using the Python API instead of subprocess calls
- **Better Error Handling**: More robust error handling and progress tracking

Lets start with system requirements.

## System Requirements

For local execution:
* Python 3.8+ <https://www.python.org/downloads/>
* FFmpeg <https://ffmpeg.org/download.html>
* Git <https://git-scm.com/downloads>

Or with Docker:
* Docker <https://www.docker.com/products/docker-desktop/>

## Installation Options

### Option 1: Local Installation

Lets start by cloning the repo. Open your terminal and type the following command:

### 1. Clone Repo

```bash
git clone https://github.com/Chugarah/Oracle.git
cd oracle
```

### 2. Install Dependencies

#### Option A: Using UV Virtual Environment (Linux/macOS)

We use UV for dependency management and virtual environments:

```bash
# Setup the development environment
./downloader/script/setup_env.sh

# Activate the environment
source downloader/script/venv/oracle-downloader/bin/activate

# Run the downloader
python ./downloader/script/main.py

# Alternatively, you can use the run_dev.sh script to activate and run in one step
./downloader/script/run_dev.sh
```

#### Option B: Using pip directly (Windows)

```bash
pip install -r ./downloader/script/requirements.txt

# Run the downloader
python ./downloader/script/main.py
```

### 3. Update Dependencies (Optional)

If you want to update yt-dlp or other dependencies to the latest version:

#### For UV Virtual Environment:
```bash
# Activate the environment
source downloader/script/venv/oracle-downloader/bin/activate

# Update yt-dlp
uv pip install --upgrade yt-dlp
```

#### For pip users:
```bash
pip install --upgrade yt-dlp
```

### Option 2: Docker Installation (Recommended)

We provide a Docker container that includes all required dependencies. You'll learn how to use it later in this document.

## Configuration Files

We need to set path from where where we want to store the files and where we should convert it from using FFmpeg. We need to edit the following files in the downloader-conf folder:

1. video_links.txt. This file is where you put your video links or playlist. Look at the example below:

    ```txt
    https://www.youtube.com/watch?v=JjBRlnO6LvA&list=PLqWxGh_2yxf_xCKNnYXfGpD10EBEv7p2Y
    https://www.youtube.com/watch?v=2DRSEQ5JBic
    ```

2. downloader-settings.json. The "inputFolder" is where the FFmpeg will look for files to convert. The rest does not need editing

    ```json
    {
        "authentication": "false",
        "config": "downloader/script/downloader-conf/yt-dlp.conf",
        "browser": "chrome",
        "videoLinks": "downloader/script/downloader-conf/video_links.txt",
        "playListVideoRaw": "downloader/script/downloader-conf/playlist-links-parser.txt",
        "linkReader": "downloader/script/downloader-conf/link-reader.txt",
        "inputFolder": "downloader/files/",
        "authCookie": "downloader/script/downloader-conf/auth/auth_cookie.txt",
        "cookieTimerPath": "downloader/script/downloader-conf/auth/cookie_timer.txt",
        "chromeProfileLocation": "C:/Users/User/AppData/Local/Google/Chrome/User Data",
        "chromeExeLocation": "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "baseSite": "https://www.youtube.com"
    }
    ```

    Detail explanation of each line:

    | Key                   | Description                                                                                                                                                                                                                          |
    | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | authentication        | Enable this to use Cookie authentication                                                                                                                                                                                             |
    | config                | The configuration file for yt-dlp location                                                                                                                                                                                           |
    | browser               | Which browser to open for to refresh our cookie authentication. Oracle supports Chrome only for the moment                                                                                                                           |
    | videoLinks            | This is the file you add your video links or playlist links.                                                                                                                                                                         |
    | playListVideoRaw      | This is file where the raw output from yt-dlp is being parsed from. This file should not be edited                                                                                                                                   |
    | linkReader            | This file is the same as playListVideoRaw, just an file to be parsed. Should not be edited                                                                                                                                           |
    | inputFolder           | This is the folder where FFmpeg will look and also our location where we store our downloaded content                                                                                                                                |
    | authCookie            | Place where your cookie data will be stored, please don't edit this                                                                                                                                                                  |
    | cookieTimerPath       | Place where the cookie timer will be stored, please don't edit this                                                                                                                                                                  |
    | chromeProfileLocation | This is the location of your chrome profile. This is used to get the cookie data. This is default storage for default user and for windows. Based if you have multiple profiles you need to change this to the profile you are using |
    | chromeExeLocation     | This is the location of your chrome.exe. This is used to open chrome to refresh the cookie. That is the default location if you don't install it in custom location.                                                                 |
    | baseSite              | This is the base site for youtube. I use .com but can be anything based on your preference but it need to be youtube.                                                                                                                |

    The line that is good to start with is "inputFolder". This is where you place the path to the folder where you want to store the files. The rest does not need editing. If you want to test or satisfied with current settings the only line needs editing is where you place the path to the folder where you want to store the files.

3. yt-dlp.conf. This is the main conf file for yt-dlp. More detail information can be found <https://github.com/yt-dlp/yt-dlp#general-options>. This settings that I provided in this modules, download the best quality video and audio and then merge them together. It also download the best audio quality.The rest does not need editing. If you want to test or satisfied with current settings the only line needs editing is where you place the path to the folder where you want to store the files.

    This is also how the files will be organized. The example below will save the files in the folder downloader/files/ and then it will create a folder for each channel, year, month and then id of the video. The file will be named as id of the video. The file extension will be the same as the original file.

    Remember we are running from root directory (oracle). So it will save the files in oracle/downloader/files/

    The lines we are interested in editing is:

    ```config
    # Download the highest video resolution and best audio quality in separate formats and then merge them. You can change this to your liking. 
    # And also download the best audio separately.
    -f "bestvideo+bestaudio/best,bestaudio"

    # Save all videos under specified directory with structured organization by channel, year, month, and id
    -o downloader/files/%(channel_id)s/%(upload_date>%Y)s/%(upload_date>%m)s/%(id)s/%(id)s.%(ext)s

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
    ```

### Running Locally

We are running the script from root directory (oracle).

```bash
python ./downloader/script/main.py
```

## Docker Usage

### Building and Running the Docker Container

Docker files are located in the `Docker/` directory inside the downloader module. To use Docker:

```bash
# Navigate to the Docker directory
cd downloader/Docker

# Build and run using Docker Compose (recommended)
docker-compose up --build

# Or run in the background
docker-compose up -d

# Alternatively, build and run manually:
docker build -t oracle-downloader -f Dockerfile ..
docker run -v $(pwd)/../downloads:/downloads oracle-downloader

# Run with a specific URL
docker run -v $(pwd)/../downloads:/downloads -e "URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ" oracle-downloader

# Run with a file containing URLs
docker run -v $(pwd)/../downloads:/downloads -v $(pwd)/../my-urls.txt:/app/urls.txt oracle-downloader
```

For more detailed Docker instructions, see the [DOCKER.md](Docker/DOCKER.md) file.

### Docker Environment Variables

| Variable           | Description                          | Default                        |
| ------------------ | ------------------------------------ | ------------------------------ |
| URL                | Single URL to download               | None                           |
| FORMAT             | Format selection for yt-dlp          | "bestvideo+bestaudio/best"     |
| OUTPUT_TEMPLATE    | Output filename template             | "/downloads/%(title)s.%(ext)s" |
| ADDITIONAL_OPTIONS | Additional options to pass to yt-dlp | ""                             |

For more advanced usage, please refer to the yt-dlp documentation: https://github.com/yt-dlp/yt-dlp
