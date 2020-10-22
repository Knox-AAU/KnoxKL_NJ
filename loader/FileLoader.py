from watcher.FileWatcher import FileWatcher
from watchdog.events import FileSystemEventHandler
from knox_source_data_io.io_handler import IOHandler, Generator, Wrapper
from loader.JsonWrapper import Publication
from environment.EnvironmentConstants import EnvironmentVariables as ev
import os, shutil

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
                try:
                    publication: Publication = load_json(event.src_path)
                    print(publication)
                    move_to_folder(event.src_path, ev().get_value(ev().OUTPUT_DIRECTORY), get_file_name_from_path(event.src_path))
                except FileExistsError as e:
                    pass # Intentional pass
                except Exception as e:
                    if os.path.exists(event.src_path):
                        print("Move file <" + event.src_path + "> with exception: " + e.__str__())
                        move_to_folder(event.src_path, ev().get_value(ev().ERROR_DIRECTORY), get_file_name_from_path(event.src_path))
                    else:
                        # Its detected as a modification when the file is moved, so it naturally fails to move when the file already has been moved
                        print("Did not find file with path <" + event.src_path + ">, it was likely moved just before...")

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

def move_to_folder(src_path: str, dest_folder: str, dest_file_name: str) -> None:
    """
    Input:
        src_path: str - The source path to the file to move
        dest_folder: str - The path to the destination folder
        dest_file_name: str - The name the file should have at the destination
    
    Moves the given file to destination
    """
    shutil.move(src=src_path, dst=f'{dest_folder}{dest_file_name}')

def get_file_name_from_path(path: str) -> str:
    """
    Input:
        path: str - The path of the file to extract the file name from
    Output:
        str - The file name from the path

    Extracts the file name from a given path
    """
    return os.path.split(path)[-1]
