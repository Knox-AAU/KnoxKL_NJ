#!/usr/bin/python3
import platform
import sys

assert platform.python_version_tuple()[1] == '8', 'This script requires python 3.8.x in order to run properly'

from loader import process_existing
import asyncio
import os
import knox_util
import logging
import logging.config
import argparse

from loader.Watcher import FileWatcher, Handler
from multiprocessing import Process
from environment.EnvironmentConstants import EnvironmentConstants as ec

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("fileLogger")
logger.info('Starting..')

input_dir = ec().get_value(ec().INPUT_DIRECTORY)
output_dir = ec().get_value(ec().OUTPUT_DIRECTORY)
err_dir = ec().get_value(ec().ERROR_DIRECTORY)

assert input_dir is not None and \
       output_dir is not None and \
       err_dir is not None, f'in:{input_dir} out:{output_dir} err:{err_dir}'

assert input_dir.endswith(('/', '\\')) and output_dir.endswith(('/', '\\')) and err_dir.endswith(('/', '\\'))

watcher = FileWatcher(input_dir)

logger.info('Finished')


def setup():
    if not os.path.exists(input_dir):
        os.mkdir(input_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if not os.path.exists(err_dir):
        os.mkdir(err_dir)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version='%(prog)s version 0.1',
                        help='Show the program version')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='info, error, warning, all')
    parser.add_argument('-l', '--debug', action='store_true', help='Starts the program with debug logging enabled')
    parser.add_argument('-m', '--model', default='sm', const='sm', nargs='?', choices=['sm', 'md', 'lg'],
                        help='Specify which model the program should use (default: %(default)s)')
    return parser


def parse_args(args, parser):
    return parser.parse_args(args)


if __name__ == "__main__":
    parser = create_parser()
    parserArgs = parse_args(sys.argv[1:], parser)
    setup()
    process_existing(input_dir)

    watcher.run(Handler())

    print('Exiting...')
