import queue
import threading
import os
import time
from modules.settings import read_yaml_config, read_media_library, get_ytdlp_options
from modules.file_handler import FolderScanner
from modules.functions import extract_video_id
from modules.downloader import download_videos_from_source
from modules.worker_ffmpeg import WorkerFFmpeg
from modules.proxy_rotator.config import ProxyRotatorConfig
from modules.proxy_rotator.proxy_server import ProxyRotatorServer


def start_proxy_rotator(config):
    """
    Initialize and start the proxy rotator server if enabled in config.

    :param config: The application configuration
    :return: The proxy rotator server instance or None if not enabled
    """
    # Check if proxy rotator is configured
    if 'proxy_rotator' not in config:
        print("Proxy rotator not configured, skipping")
        return None

    # Create configuration object
    proxy_config = ProxyRotatorConfig(config['proxy_rotator'])

    # Validate configuration
    if not proxy_config.validate():
        print("Proxy rotator configuration is invalid, skipping")
        return None

    if not proxy_config.enabled:
        print("Proxy rotator is disabled in configuration, skipping")
        return None

    # Initialize the server
    server = ProxyRotatorServer(proxy_config)

    # Start the server
    if server.start():
        print(f"Proxy rotator server started at {server.proxy_url}")

        # Update yt-dlp options if server started successfully
        if 'ytdlp' not in config:
            config['ytdlp'] = {}

        # Add the proxy to the default options
        if 'default' not in config['ytdlp']:
            config['ytdlp']['default'] = {}

        # Set the proxy URL for yt-dlp
        config['ytdlp']['default']['proxy'] = server.proxy_url

        return server
    else:
        print("Failed to start proxy rotator server")
        return None


def stop_proxy_rotator(server):
    """
    Stop the proxy rotator server.

    :param server: The proxy rotator server instance
    """
    if server:
        server.stop()
        print("Proxy rotator server stopped")


def main():
    """
    Main function to run the downloader application.
    """
    print("Starting YT-DLP Downloader")

    # Load configuration
    config = read_yaml_config()
    media_library = read_media_library()

    if not media_library:
        print("No media sources found in the media library. Please add some URLs to media-library.json.")
        return

    # Check if any sources are enabled
    enabled_sources = [source for source, data in media_library.items()
                       if data.get('config', {}).get('enabled', True)]

    if not enabled_sources:
        print("No enabled sources found in the media library. Please enable at least one source.")
        return

    # Start proxy rotator if configured
    proxy_server = start_proxy_rotator(config)

    # Get thread count from config
    thread_count = config.get('app', {}).get('download_threads', 3)
    print(f"Using {thread_count} download threads")

    # Create a thread pool for downloads
    threads = []

    try:
        # Process each source in the media library
        for source_type, source_data in media_library.items():
            # Skip if no config or items
            if 'config' not in source_data or 'items' not in source_data:
                print(
                    f"Skipping {source_type} as it has invalid configuration")
                continue

            source_config = source_data['config']
            items = source_data['items']

            # Skip if disabled or no items
            if not source_config.get('enabled', True) or not items:
                print(
                    f"Skipping {source_type} as it is disabled or has no items")
                continue

            print(f"Processing {source_type} source")

            # Get YT-DLP options for this source
            ytdlp_options = get_ytdlp_options(
                config, source_type, source_config)

            # Create and start a thread for this source
            t = threading.Thread(
                target=download_videos_from_source,
                args=(source_type, source_config, ytdlp_options, items)
            )
            threads.append(t)
            t.start()

            # Limit concurrent threads
            while sum(t.is_alive() for t in threads) >= thread_count:
                time.sleep(0.5)

        # Wait for all download threads to complete
        for t in threads:
            t.join()

        print("All downloads completed")

        # Check if FFMPEG post-processing is enabled
        if config.get('app', {}).get('ffmpeg', {}).get('enabled', True):
            print("Starting FFMPEG post-processing")
            worker_ffmpeg = WorkerFFmpeg()
            worker_ffmpeg.start()
            worker_ffmpeg.join()
            print("FFMPEG post-processing completed")

        print("Downloader process completed successfully")

    finally:
        # Always stop the proxy server when we're done
        stop_proxy_rotator(proxy_server)


if __name__ == '__main__':
    main()
