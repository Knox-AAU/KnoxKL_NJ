import knox_util, os

@knox_util.background_process
def process_existing(path: str) -> None:
    print(f'Checking for existing files in \'{path}\'...')
    paths = [os.path.join(path, fn) for fn in next(os.walk(path))[2]]
    if len(paths) == 0:
        print('No files were created between sessions')
        return