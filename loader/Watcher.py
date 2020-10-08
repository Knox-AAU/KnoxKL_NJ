from __future__ import annotations

import time

import knox_util

from os import path
from loader import JsonLoader
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



class FileWatcher:
    """
    Class used to watch a directory for file changes
    The class will call the FileSystem handler
    """
    __watch_dir__: str = "DOES NOT EXIST"

    def __init__(self, path: str):
        self.observer = Observer()
        self.__watch_dir__ = path

    def run(self, handler):
        """
        Runnable method that starts the watcher.
        """

        assert self.__watch_dir__ != "DOES NOT EXIST"
        assert path.exists(self.__watch_dir__)

        self.handler = handler

        print(f'Watching directory \'{self.__watch_dir__}\' for new publication files')

        self.observer.schedule(self.handler, self.__watch_dir__, recursive=True)
        self.observer.start()
        self.isRunning = True
        try:
            while self.observer.isAlive():
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Watcher stopped successfully")
        except:
            self.observer.stop()
            print("Watcher stopped unexpectedly")

        self.observer.join()

    def stop(self):
        """
        Stops the watcher
        """
        self.observer.stop()
        print('Watcher stopped successfully')
        self.observer.join()
    



class Handler(FileSystemEventHandler):
    """
    This class handles events in the filesystem.
    """

    @staticmethod
    def on_any_event(event):
        """
        Event handler for file specific events.
        """
        if event.is_directory:
            return None  

        elif event.event_type == 'modified':
            if event.src_path.endswith('.json'):
                print('Received file', event.src_path)
                news = JsonLoader.load_json(event.src_path)
                news.load_publications()
                
