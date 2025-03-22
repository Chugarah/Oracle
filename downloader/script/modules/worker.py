import threading

from modules.downloader import download_video
from modules.functions import generate_youtube_url


class Worker(threading.Thread):
    def __init__(self, video_id, config, total_links, file_counter, result):
        super().__init__()
        self.video_id = video_id
        self.config = config
        self.total_links = total_links
        self.file_counter = file_counter
        self.result = result

    def run(self):
        video_url = generate_youtube_url(self.video_id)
        download_video(video_url, self.config, self.video_id,
                       self.total_links, self.file_counter)
        return
