
from multiprocessing import Process
from modules.playlist_core import PlayListCore


class GeneratePlayList(Process):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        PlayListCore.play_list_init(self.config)
