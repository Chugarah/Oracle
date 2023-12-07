import queue
from modules.worker import Worker
from modules.worker_ffmpeg import Worker_ffmpeg
from modules.settings import read_settings
from modules.playlist import GeneratePlayList
from modules.file_handler import FolderScanner
from modules.functions import extract_video_id
import os


def main():
    settings = read_settings()
    file_counter = 1
    q = queue.Queue()

    play_list_worker = GeneratePlayList(settings)
    q.put(play_list_worker)

    while not q.empty():
        worker = q.get()
        worker.start()
        worker.join()

    result = FolderScanner.scan_folder(
        settings['inputFolder'], ['.webm'])
    downloaded_ids = set(item[2] for item in result)

    with open(settings['linkReader'], 'r') as f:
        f.seek(0)

        link_ids = set()
        for line in f:
            video_id = extract_video_id(line.strip())
            link_ids.add(video_id)

        missing_ids = link_ids - downloaded_ids
        total_links = len(missing_ids)

        for video_id in missing_ids:

            worker = Worker(video_id, settings, total_links,
                            file_counter, downloaded_ids)
            q.put(worker)
            downloaded_ids.add(video_id)
            file_counter += 1

    while not q.empty():
        worker = q.get()
        worker.start()
        worker.join()

    worker_ffmpeg = Worker_ffmpeg()
    worker_ffmpeg.start()
    worker_ffmpeg.join()


if __name__ == '__main__':
    main()
