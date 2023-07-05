import json
import queue
from modules.worker import Worker
from modules.worker_ffmpeg import Worker_ffmpeg
from modules.settings import read_settings
from modules.playlist import GeneratePlayList


def main():
    # Read settings
    settings = read_settings()

    with open(settings['videoLinks'], 'r') as f:
        youtube_links = json.load(f)

    # Ensure that the Worker objects start and finish sequentially
    q = queue.Queue()  # create a queue

    # Create an additional Worker object
    play_list_worker = GeneratePlayList(settings)
    q.put(play_list_worker)

    # Create a Worker object for each link and put them in the queue
    for link in youtube_links:
        worker = Worker(link)
        q.put(worker)

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
