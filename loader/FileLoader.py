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

        elif event.event_type == 'modified' or event.event_type == 'created':
            if event.src_path.endswith('.json'):    
                # TODO Fix so that this is a single method call
                try:
                    publication: Publication = load_json(event.src_path)
                    print(publication)
                    move_file(event.src_path, ev().get_value(ev().OUTPUT_DIRECTORY), get_file_name_from_path(event.src_path))
                except FileExistsError as e:
                    pass # Intentional pass
                except Exception as e:
                    if os.path.exists(event.src_path):
                        print(f'Move file <{event.src_path}> with exception:',e)
                        move_file(event.src_path, ev().get_value(ev().ERROR_DIRECTORY), get_file_name_from_path(event.src_path))
                    else:
                        # Its detected as a modification when the file is moved, so it naturally fails to move when the file already has been moved
                        print("Did not find file with path <" + event.src_path + ">, it was likely moved just before...")


def process_existing(path: str) -> None:
    """
    Input:
        path: str - The input directory path, that will be processed

    This method will look through the input directory, and determine whether a file has been processed previously
    When the file has been processed, it will be moved to the output directory.
    """
    print(f'Checking for existing files in \'{path}\'...')
    paths = [os.path.join(path, fn) for fn in next(os.walk(path))[2]]
    if len(paths) == 0:
        print('No files were created between sessions')
        return

    for path in paths:
        
        # Process files here
        split_path = os.path.split(path)

        try:
            # TODO create separate function to handle this
            news = load_json(path)

            move_file(path, ev().get_value(ev().OUTPUT_DIRECTORY), split_path[-1])
        except Exception as e:
            print(f'Move file <{path}> with exception:',e)
            move_file(path, ev().get_value(ev().ERROR_DIRECTORY), split_path[-1])


    # Simulated finished



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
        return Publication(wrap['content'])

def start_watch_directory(directory: str):
    """
    Input:
        directory: str - The directory to watch for file changes in.
    
    This function starts a file watcher to process files in a given directory.
    """
    file_watcher = FileWatcher(directory)
    file_watcher.run(Handler())

def move_file(src_path: str, dest_folder: str, dest_file_name: str) -> None:
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
