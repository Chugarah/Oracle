import queue
import threading
import os
import time
from modules.settings import read_yaml_config, read_media_library, get_ytdlp_options
from modules.file_handler import FolderScanner
from modules.functions import extract_video_id
from modules.downloader import download_videos_from_source
from modules.worker_ffmpeg import WorkerFFmpeg


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

    # Get thread count from config
    thread_count = config.get('app', {}).get('download_threads', 3)
    print(f"Using {thread_count} download threads")

    # Create a thread pool for downloads
    threads = []

    # Process each source in the media library
    for source_type, source_data in media_library.items():
        # Skip if no config or items
        if 'config' not in source_data or 'items' not in source_data:
            print(f"Skipping {source_type} as it has invalid configuration")
            continue

        source_config = source_data['config']
        items = source_data['items']

        # Skip if disabled or no items
        if not source_config.get('enabled', True) or not items:
            print(f"Skipping {source_type} as it is disabled or has no items")
            continue

        print(f"Processing {source_type} source")

        # Get YT-DLP options for this source
        ytdlp_options = get_ytdlp_options(config, source_type, source_config)

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


if __name__ == '__main__':
    main()
