import json
import queue
from modules.worker import Worker
from modules.worker_ffmpeg import Worker_ffmpeg
from modules.settings import read_settings
from modules.playlist import GeneratePlayList


def main():
    # Read settings
    settings = read_settings()
    file_counter = 1

    # Ensure that the Worker objects start and finish sequentially
    q = queue.Queue()  # create a queue

    # Create an additional Worker object
    play_list_worker = GeneratePlayList(settings)
    q.put(play_list_worker)

    # Start each Worker object in the queue, one by one
    while not q.empty():
        worker = q.get()
        worker.start()
        worker.join()  # wait for the current thread to complete

    # Open the text file
    with open(settings['videoLinks'], 'r') as f:
        # Read the file line by line
        total_links = len(f.readlines())
        f.seek(0)  # Reset file pointer to the beginning
        for line in f:
            # Convert each line from JSON to text
            video_id = line.strip()  # Assuming each line contains a single video ID
            worker = Worker(video_id, settings, total_links, file_counter)
            q.put(worker)
            file_counter += 1

    # Start each Worker object in the queue, one by one
    while not q.empty():
        worker = q.get()
        worker.start()
        worker.join()  # wait for the current thread to complete

    # Once all the Worker threads are completed, start the Worker_ffmpeg
    worker_ffmpeg = Worker_ffmpeg()
    worker_ffmpeg.start()
    worker_ffmpeg.join()  # wait for the Worker_ffmpeg thread to finish


if __name__ == '__main__':
    main()
