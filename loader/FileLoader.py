from watcher.FileWatcher import FileWatcher
from watchdog.events import FileSystemEventHandler
from knox_source_data_io.io_handler import IOHandler, Generator, Wrapper
from loader.JsonWrapper import Publication

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
                # TODO Fix so that this is a single method call
                publication: Publication = load_json(event.src_path)
                print(publication)

def load_json(json_path: str) -> Publication:
    """
    Input:
        json_path: str - The path to the json news struct
    
    Returns:
        A publication parsed from the input file
    
    This function creates and loads a news struct into memort
    """
    handler = IOHandler(Generator(app="This app", version=1.0), "https://repos.libdom.net/schema/publication.schema.json")
    with open(json_path, "r", encoding="utf-8") as json_file:
        wrap: Wrapper = handler.read_json(json_file)
        return Publication(wrap["content"])

def start_watch_directory(directory: str):
    """
    Input:
        directory: str - The directory to watch for file changes in.
    
    This function starts a file watcher to process files in a given directory.
    """
    file_watcher = FileWatcher(directory)
    file_watcher.run(Handler())
