import knox_util, os

from environment.EnvironmentConstants import EnvironmentVariables as ev
from loader.FileLoader import load_json, move_to_folder

def process_existing(path: str, output_path: str, error_path: str) -> None:
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

            shutil.move(src=path, dst=f'{output_path}{split_path[-1]}')
        except Exception as e:
            print(e)
            #shutil.move(src=path, dst=f'{error_path}{split_path[-1]}')

    print('Finished processing files created between sessions')
    # Simulated finished
