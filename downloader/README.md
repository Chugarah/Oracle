# Module : Media Downloader

Welcome traveler, to the media downloader module. This module is using yt-dlp to download videos from YouTube and other platforms. The module is using Python and can run both locally or via Docker. Previously it supported Windows environments only, but now it supports both Windows and Linux via Docker.

## Recent Updates

- **New Configuration System**: Implemented YAML configuration and JSON media library for easier management
- **Improved Progress Tracking**: Now using yt-dlp's built-in progress hooks for more accurate download progress reporting
- **API-Based Integration**: Enhanced integration with yt-dlp using the Python API instead of subprocess calls
- **Better Error Handling**: More robust error handling and progress tracking
- **Multi-Source Support**: Organized download structure by source type (YouTube, TikTok, etc.)
- **Fixed Progress Bar Issue**: Resolved the "not supported between instances of float and str" error by using minimal yt-dlp configuration

Let's start with system requirements.

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
uv pip install -r ./downloader/script/requirements.txt
```

#### For pip users:
```bash
pip install --upgrade yt-dlp
```

### Option 2: Docker Installation (Recommended)

We provide a Docker container that includes all required dependencies. You'll learn how to use it later in this document.

## Configuration System

The downloader now uses a modern configuration system with two main files:

### YAML Configuration (`config.yaml`)

The main configuration file uses YAML format for better readability and organization:

```yaml
# Application settings
app:
  download_threads: 3
  check_existing: true
  log_level: "info"
  ffmpeg:
    enabled: true
    threads: 2
    additional_options: "-c:v libx264 -c:a aac"

# YT-DLP base settings
ytdlp:
  authentication:
    enabled: false
    cookie_file: "auth/cookies.txt"
  proxy:
    enabled: false
    url: ""
  rate_limit: "0"  # 0 = unlimited
  retry_count: 3
  user_agent: ""
  progress_options:
    # Display options
    quiet: false                # Activate quiet mode
    verbose: false              # Print debugging information
    no_warnings: false          # Ignore warnings
    
    # Download control
    simulate: false             # Do not download the video
    skip_download: false        # Write related files but don't download video
    
    # Output formats
    dump_json: false            # Print JSON information for each video
    dump_single_json: false     # Print JSON information for each URL or infojson
    
    # Progress bar options
    no_progress: false          # Do not print progress bar
    progress: true              # Show progress bar, even in quiet mode
    console_title: true         # Display progress in console titlebar
    newline: false              # Output progress bar as new lines

# Source-specific YT-DLP options
sources:
  youtube:
    format: "bestvideo+bestaudio/best"
    subtitles: "en"
    embed_metadata: true
    output_template: "downloads/youtube/%(channel_id)s/%(upload_date>%Y)s/%(upload_date>%m)s/%(id)s/%(id)s.%(ext)s"
    progress_options:
      # Override global progress options for this source
      console_title: true
  
  tiktok:
    format: "best"
    embed_metadata: true
    output_template: "downloads/tiktok/%(uploader)s/%(id)s.%(ext)s"
  
  # You can add more sources with custom settings
```

### JSON Media Library (`media-library.json`)

The URLs to download are organized in a JSON structure by source type:

```json
{
  "youtube": {
    "config": {
      "enabled": true,
      "max_downloads": 0,
      "prefer_config": "source",
      "progress_options": {
        "console_title": true,
        "progress_template": "download:[%(info.id)s] %(progress.eta)s %(progress._percent_str)s",
        "newline": false
      }
    },
    "items": [
      {
        "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw"
      },
      {
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
      }
    ]
  },
  "tiktok": {
    "config": {
      "enabled": false,
      "max_downloads": 10,
      "prefer_config": "custom",
      "custom_format": "best"
    },
    "items": [
      {
        "url": "https://www.tiktok.com/@username/video/VIDEO_ID"
      }
    ]
  }
}
```

### Configuration Options

#### Source Configuration

Each source in the media library can have these configuration options:

- `enabled`: Enable/disable this source type (boolean)
- `max_downloads`: Limit number of downloads from this source (0 = unlimited)
- `prefer_config`: Which configuration to use ("source", "custom", or "default")
- `custom_format`: Custom format string if using custom config
- `custom_output_template`: Custom output template if using custom config

#### Common YT-DLP Options

The most common YT-DLP options are exposed in the YAML configuration:

- `format`: Format selection (e.g., "bestvideo+bestaudio/best")
- `output_template`: Template for output filenames
- `subtitles`: Subtitle language(s) to download
- `embed_metadata`: Whether to embed thumbnails and metadata in the output file

## Adding New Sources

To add a new source for downloading:

1. Add the source type to your `media-library.json` file
2. Configure source-specific settings in `config.yaml` if needed
3. Add URLs to the `items` array for that source type

The downloader will automatically detect and process each source according to its configuration.

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

## Troubleshooting

### Progress Bar Error: "not supported between instances of float and str"

If you encounter the error "'>' not supported between instances of 'float' and 'str'" during downloads, this is related to a type mismatch in the progress tracking system. The issue has been fixed by:

1. Using a more minimal approach with yt-dlp's built-in progress display
2. Removing custom progress hooks that could cause type conversion issues
3. Simplifying the download options to focus on essential parameters

This solution ensures reliable downloads while maintaining progress visibility. If you still encounter this error, try updating to the latest version of yt-dlp using:

```bash
pip install -U yt-dlp
```

If problems persist, you can modify `downloader.py` to further simplify the options passed to yt-dlp by removing any custom progress or formatting configurations.

## Progress Options

The application supports various progress display options from yt-dlp. These can be configured at three levels:

1. **Global level** in `config.yaml` under the `ytdlp.progress_options` section
2. **Source level** in `config.yaml` under `sources.<source_name>.progress_options`
3. **Item level** in `media-library.json` for individual videos

Available progress options include:

| Option          | Description                                       |
| --------------- | ------------------------------------------------- |
| `quiet`         | Activate quiet mode to suppress most output       |
| `verbose`       | Enable verbose logging for debugging              |
| `no_warnings`   | Suppress warning messages                         |
| `simulate`      | Simulate the download without writing files       |
| `skip_download` | Write metadata but skip the actual video download |
| `no_progress`   | Disable the progress bar                          |
| `progress`      | Always show progress even in quiet mode           |
| `console_title` | Show download progress in the console title bar   |
| `newline`       | Print progress bars on new lines                  |

Example configuration:

```yaml
# In config.yaml
ytdlp:
  progress_options:
    quiet: false
    console_title: true
    newline: false
```

```json
// In media-library.json
{
  "youtube": {
    "config": {
      "progress_options": {
        "console_title": true
      }
    },
    "items": [
      {
        "url": "https://www.youtube.com/watch?v=VIDEO_ID",
        "options": {
          "progress_options": {
            "newline": true
          }
        }
      }
    ]
  }
}
```

### Setting Up config.yaml

The `config.yaml` file contains the following sections:

```yaml
# Application settings
app:
  download_threads: 3  # Number of concurrent downloads
  check_existing: true  # Skip already downloaded videos
  log_level: "info"  # Logging level
  ffmpeg:
    enabled: true  # Enable FFMPEG post-processing
    threads: 2  # Number of FFMPEG threads
    additional_options: "-c:v libx264 -c:a aac"  # Additional FFMPEG options

# YT-DLP base settings
ytdlp:
  authentication:
    enabled: false  # Enable authentication
    cookie_file: "auth/cookies.txt"  # Path to cookie file
  proxy:
    enabled: false  # Enable proxy
    url: ""  # Proxy URL
  rate_limit: "25000"  # Download rate limit (0 = unlimited)
  retry_count: 3  # Number of retries
  user_agent: "Mozilla/5.0..."  # User agent string
  progress_options:
    # Display options
    quiet: false                # Activate quiet mode
    verbose: false              # Print debugging information
    no_warnings: false          # Ignore warnings
    
    # Download control
    simulate: false             # Do not download the video
    skip_download: false        # Write related files but don't download video
    
    # Output formats
    dump_json: false            # Print JSON information for each video
    dump_single_json: false     # Print JSON information for each URL or infojson
    
    # Progress bar options
    no_progress: false          # Do not print progress bar
    progress: true              # Show progress bar, even in quiet mode
    console_title: true         # Display progress in console titlebar
    newline: false              # Output progress bar as new lines

# Source-specific settings
sources:
  youtube:
    format: "best"  # Default format to download
    subtitles: "en"  # Default subtitle language
    embed_metadata: true  # Embed metadata in downloaded file
    output_template: "downloads/youtube/%(channel_id)s/%(upload_date>%Y)s/%(upload_date>%m)s/%(id)s/%(id)s.%(ext)s"
    progress_options:
      # Override global progress options for this source
      console_title: true
```

### Setting Up media-library.json

The `media-library.json` file contains the sources and URLs to download:

```json
{
  "youtube": {
    "config": {
      "enabled": true,
      "prefer_config": "source",
      "progress_options": {
        "console_title": true
      }
    },
    "items": [
      {
        "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",
        "id": "jNQXAC9IVRw",
        "title": "Me at the zoo",
        "options": {
          "progress_options": {
            "console_title": true,
            "newline": false
          }
        }
      }
    ]
  }
}
```

## Usage

Run the application with:

```
python script/main.py
```

The application will:
1. Read the configuration files
2. Download videos from enabled sources
3. Apply FFMPEG post-processing if enabled

## Docker Usage

To run the application in Docker:

```
docker build -t yt-dlp-downloader .
docker run -v /path/to/downloads:/downloads yt-dlp-downloader
```

## Notes

- The application uses a multi-threaded approach to download videos concurrently
- FFMPEG post-processing is optional and can be disabled
- Cookies file may be required for some platforms with authentication
- Progress display options can be customized extensively

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Media Library Configuration

The media library is defined in `downloader-conf/media-library.json`. This file contains a list of sources and videos to download.

### Simplified Format (Recommended)

The simplified format only requires URLs, with all configuration at the source level:

```json
{
  "youtube": {
    "config": {
      "enabled": true,
      "max_downloads": 0,
      "prefer_config": "source",
      "progress_options": {
        "console_title": true,
        "progress_template": "download:[%(info.id)s] %(progress.eta)s %(progress._percent_str)s",
        "newline": false
      }
    },
    "items": [
      {
        "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw"
      },
      {
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
      }
    ]
  }
}
```

### Source Configuration

Each source has a `config` section with the following options:

- `enabled`: Whether this source is enabled for downloading
- `max_downloads`: Maximum number of videos to download (0 = unlimited)
- `prefer_config`: Which configuration to use ("source", "custom", or "default")
- `progress_options`: Options for progress reporting

### Progress Options

The progress options are passed to YT-DLP and control how download progress is displayed:

- `console_title`: Display progress in console titlebar
- `progress_template`: Custom template for progress display
- `newline`: Output progress bar as new lines
- And other YT-DLP progress options

### Legacy Format (Deprecated)

The older format with item-level options is still supported but deprecated:

```json
{
  "youtube": {
    "config": {
      "enabled": true
    },
    "items": [
      {
        "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",
        "id": "jNQXAC9IVRw",
        "title": "Me at the zoo",
        "options": {
          "progress_options": {
            "console_title": true
          }
        }
      }
    ]
  }
}
```

Note: Item-level `id` and `title` fields are no longer needed as they are extracted automatically.
