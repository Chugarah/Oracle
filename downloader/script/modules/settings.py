import json
import os
import yaml
from typing import Dict, Any, Optional


def get_base_directory():
    """
    Get the base directory of the script.

    :return: The path to the base directory
    """
    script_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_directory)


def read_yaml_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Read the YAML configuration file.

    :param config_path: Optional path to the config file. If not provided, uses the default path.
    :return: Dictionary containing the configuration
    """
    if config_path is None:
        base_dir = get_base_directory()
        config_path = os.path.join(base_dir, 'downloader-conf', 'config.yaml')

    # Check if running in Docker environment
    if os.environ.get('DOCKER_ENV') == 'true':
        # If config path is provided through environment variable, use that instead
        config_path = os.environ.get('CONFIG_PATH', config_path)

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Warning: Configuration file not found at {config_path}")


def read_media_library(library_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Read the JSON media library file.

    :param library_path: Optional path to the library file. If not provided, uses the default path.
    :return: Dictionary containing the media library
    """
    if library_path is None:
        base_dir = get_base_directory()
        library_path = os.path.join(
            base_dir, 'downloader-conf', 'media-library.json')

    # Check if running in Docker environment
    if os.environ.get('DOCKER_ENV') == 'true':
        # If library path is provided through environment variable, use that instead
        library_path = os.environ.get('MEDIA_LIBRARY_PATH', library_path)

    try:
        with open(library_path, 'r') as f:
            library = json.load(f)
        return library
    except FileNotFoundError:
        print(
            f"Warning: Media library file not found at {library_path}. Using empty library.")
        # Return empty library if file not found
        return {}


def get_source_settings(config: Dict[str, Any], source_type: str) -> Dict[str, Any]:
    """
    Get settings for a specific source type from the configuration.

    :param config: The full configuration dictionary
    :param source_type: The type of source (e.g., "youtube", "tiktok")
    :return: Dictionary containing settings for the specified source
    """
    # Get default source settings
    default_settings = config.get('sources', {}).get('default', {})

    # Get source-specific settings or empty dict if not found
    source_settings = config.get('sources', {}).get(source_type, {})

    # Merge default settings with source-specific settings
    # Source-specific settings take precedence
    merged_settings = {**default_settings, **source_settings}

    return merged_settings


def get_ytdlp_options(config: Dict[str, Any], source_type: str, source_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert configuration settings to YT-DLP options.

    :param config: The full configuration dictionary
    :param source_type: The type of source (e.g., "youtube", "tiktok")
    :param source_config: The source-specific configuration from the media library
    :return: Dictionary containing YT-DLP options
    """
    # Get base YT-DLP settings
    ytdlp_config = config.get('ytdlp', {})

    # Get source-specific settings
    source_settings = get_source_settings(config, source_type)

    # Determine which config to use based on source_config's prefer_config
    prefer_config = source_config.get('prefer_config', 'source')

    # Initialize options dict
    options = {}

    # Add authentication settings if enabled
    if ytdlp_config.get('authentication', {}).get('enabled', False):
        options['cookiefile'] = ytdlp_config.get(
            'authentication', {}).get('cookie_file')

    # Add proxy settings if enabled
    if ytdlp_config.get('proxy', {}).get('enabled', False):
        options['proxy'] = ytdlp_config.get('proxy', {}).get('url')

    # Add rate limit if specified
    rate_limit = ytdlp_config.get('rate_limit')
    if rate_limit and rate_limit != '0':
        options['ratelimit'] = rate_limit

    # Add sleep intervals if specified
    sleep_interval = ytdlp_config.get('sleep_interval')
    if sleep_interval:
        options['sleep_interval'] = sleep_interval

    max_sleep_interval = ytdlp_config.get('max_sleep_interval')
    if max_sleep_interval:
        options['max_sleep_interval'] = max_sleep_interval

    sleep_requests = ytdlp_config.get('sleep_requests')
    if sleep_requests:
        options['sleep_requests'] = sleep_requests

    # Add retry count
    options['retries'] = ytdlp_config.get('retry_count', 3)

    # Add user agent if specified
    user_agent = ytdlp_config.get('user_agent')
    if user_agent:
        options['user_agent'] = user_agent

    # Add SSL certificate verification option (disable to fix SSL errors)
    options['nocheckcertificate'] = True

    # Get progress options from config
    progress_options = ytdlp_config.get('progress_options', {})

    # Store progress options as a separate field that will be processed by download_video
    # We keep them separate to avoid conflicts with yt-dlp option names
    if progress_options:
        options['progress_options'] = progress_options

    # Add source-specific settings
    if prefer_config == 'source' or prefer_config == 'default':
        # Use a format that doesn't require ffmpeg for merging
        if source_type == 'youtube':
            # Use 'best' instead of 'bestvideo+bestaudio/best'
            options['format'] = 'best'
        else:
            options['format'] = source_settings.get('format', 'best')

        options['outtmpl'] = source_settings.get('output_template')

        if source_settings.get('subtitles'):
            options['writesubtitles'] = True
            options['subtitleslangs'] = [source_settings.get('subtitles')]

        if source_settings.get('embed_metadata', False):
            options['writethumbnail'] = True
            options['embed_thumbnail'] = True
            options['addmetadata'] = True

    # If custom config is preferred, use settings from the media library
    elif prefer_config == 'custom':
        if source_config.get('custom_format'):
            options['format'] = source_config.get('custom_format')

        if source_config.get('custom_output_template'):
            options['outtmpl'] = source_config.get('custom_output_template')

    # Add any source-specific progress options
    if source_config.get('progress_options'):
        # If source has progress_options, merge them with global progress_options
        if 'progress_options' not in options:
            options['progress_options'] = {}

        options['progress_options'].update(
            source_config.get('progress_options'))

    return options


def read_legacy_settings():
    """
    Read the legacy JSON settings file for backward compatibility.

    :return: Dictionary containing the legacy settings
    """
    base_dir = get_base_directory()
    file_path = os.path.join(base_dir, 'downloader-conf',
                             'downloader-settings.json')

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
        try:
            with open(file_path, 'r') as f:
                settings = json.load(f)
        except FileNotFoundError:
            print(
                f"Warning: Legacy settings file not found at {file_path}. Using default settings.")
            settings = {}

    return settings


# For backward compatibility
read_settings = read_legacy_settings
