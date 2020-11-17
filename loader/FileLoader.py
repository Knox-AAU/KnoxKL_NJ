from watcher.FileWatcher import FileWatcher
from watchdog.events import FileSystemEventHandler
from knox_source_data_io.io_handler import IOHandler, Generator, Wrapper
from knox_source_data_io.models.publication import Publication
from environment.EnvironmentConstants import EnvironmentVariables as ev
import os, shutil
from knox_util import print
from extractor.TripleExtractor import TripleExtractor

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
            print(f'FileWatcher captured a directory_{event.event_type} event', 'debug')
            return None  

        elif event.event_type == 'modified' or event.event_type == 'created':
            print(f'FileWatcher captured a file_{event.event_type} event', 'debug')
            if event.src_path.endswith('.json'):
                print('It was a json file that caused the event', 'debug')
                # TODO Fix so that this is a single method call
                try:
                    publication: Publication = load_json(event.src_path)
                    TripleExtractor('da_core_news_lg').process_publication(publication)
                    move_file(event.src_path, ev.instance.get_value(ev.instance.OUTPUT_DIRECTORY), get_file_name_from_path(event.src_path))
                except FileExistsError as e:
                    pass # Intentional pass
                except Exception as e:
                    if os.path.exists(event.src_path):
                        print(f'Move file <{event.src_path}> with exception: {e}', 'error')
                        move_file(event.src_path, ev.instance.get_value(ev.instance.ERROR_DIRECTORY), get_file_name_from_path(event.src_path))
                    else:
                        # Its detected as a modification when the file is moved, so it naturally fails to move when the file already has been moved
                        print("Did not find file with path <" + event.src_path + ">, it was likely moved just before...", 'warning')


def process_existing(input_path: str, output_path: str, err_path: str) -> None:
    """
    Input:
        path: str - The input directory path, that will be processed

    This method will look through the input directory, and determine whether a file has been processed previously
    When the file has been processed, it will be moved to the output directory.
    """
    print(f'Checking for existing files in \'{input_path}\'...')
    paths = [os.path.join(input_path, fn) for fn in next(os.walk(input_path))[2]]
    if len(paths) == 0:
        print('No files were created between sessions', 'info')
        return

    for path in paths:
        
        # Process files here
        split_path = os.path.split(path)

        try:
            # TODO create separate function to handle this
            news = load_json(path)
            TripleExtractor('da_core_news_lg').process_publication(news)
            move_file(path, ev.instance.get_value(output_path), split_path[-1])
        except Exception as e:
            print(f'Move file <{path}> with exception: {e}', 'warning')
            move_file(path, ev.instance.get_value(err_path), split_path[-1])


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
        return wrap.content

def start_watch_directory(directory: str):
    """
    Input:
        directory: str - The directory to watch for file changes in.
    
    This function starts a file watcher to process files in a given directory.
    """
    print(f'Starting FileWatcher in directory {directory}', 'debug')
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
    print(f'Moving file {src_path} -> {dest_folder}{dest_file_name}', 'debug')
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
