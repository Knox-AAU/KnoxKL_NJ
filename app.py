#!/usr/bin/python3
import platform

assert platform.python_version_tuple()[1] == '8'

from loader import process_existing
import asyncio
import os
import knox_util


from loader.Watcher import FileWatcher, Handler
from multiprocessing import Process

input_dir = './input'
output_dir = './output'
err_dir = './err'
watcher = FileWatcher(input_dir)

@knox_util.background_process
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
    