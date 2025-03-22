import json
import os


def read_settings():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(script_directory)

    # Check if running in Docker environment
    if os.environ.get('DOCKER_ENV') == 'true':
        # If in Docker, use environment variables or default settings
        settings = {
            "authentication": os.environ.get('AUTHENTICATION', 'false'),
            "config": os.environ.get('CONFIG', 'downloader/script/downloader-conf/yt-dlp.conf'),
            "browser": os.environ.get('BROWSER', 'chrome'),
            "videoLinks": os.environ.get('VIDEO_LINKS', 'downloader/script/downloader-conf/video_links.txt'),
            "playListVideoRaw": os.environ.get('PLAYLIST_VIDEO_RAW', 'downloader/script/downloader-conf/playlist-links-parser.txt'),
            "linkReader": os.environ.get('LINK_READER', 'downloader/script/downloader-conf/link-reader.txt'),
            "inputFolder": os.environ.get('INPUT_FOLDER', '/downloads'),
            "authCookie": os.environ.get('AUTH_COOKIE', 'downloader/script/downloader-conf/auth/auth_cookie.txt'),
            "cookieTimerPath": os.environ.get('COOKIE_TIMER_PATH', 'downloader/script/downloader-conf/auth/cookie_timer.txt'),
            "chromeProfileLocation": os.environ.get('CHROME_PROFILE_LOCATION', ''),
            "chromeExeLocation": os.environ.get('CHROME_EXE_LOCATION', ''),
            "baseSite": os.environ.get('BASE_SITE', 'https://www.youtube.com')
        }
    else:
        # Read settings from file
        file_path = os.path.join(
            parent_directory, 'downloader-conf', 'downloader-settings.json')

        with open(file_path, 'r') as f:
            settings = json.load(f)

    return settings
