#!/usr/bin/python3
import platform

assert platform.python_version_tuple()[1] == '8', 'This script requires python 3.8.x in order to run properly'

from loader import process_existing
import asyncio
import os
import knox_util


from loader.Watcher import FileWatcher, Handler
from multiprocessing import Process
from environment.EnvironmentConstants import EnvironmentConstants as ec

input_dir = ec().get_value(ec().INPUT_DIRECTORY)
output_dir = ec().get_value(ec().OUTPUT_DIRECTORY)
err_dir = ec().get_value(ec().ERROR_DIRECTORY)

assert input_dir is not None and \
    output_dir is not None and \
        err_dir is not None, f'in:{input_dir} out:{output_dir} err:{err_dir}'

assert input_dir.endswith(('/','\\')) and output_dir.endswith(('/','\\')) and err_dir.endswith(('/','\\'))

watcher = FileWatcher(input_dir)

def setup():
    if not os.path.exists(input_dir):
        os.mkdir(input_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if not os.path.exists(err_dir):
        os.mkdir(err_dir)

if __name__ == "__main__":
    setup()
    process_existing(input_dir)

    watcher.run(Handler())

    print('Exiting...')
    
