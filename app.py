#!/usr/bin/python3
import platform

assert platform.python_version_tuple()[1] == '8', 'This script requires python 3.8.x in order to run properly'

import sys
import subprocess
from loader import process_existing
import asyncio
import os
import knox_util
import logging
import logging.config
import argparse

from loader.FileLoader import start_watch_directory
from multiprocessing import Process
from environment.EnvironmentConstants import EnvironmentVariables as ev

input_dir = ev().get_value(ev().INPUT_DIRECTORY)
output_dir = ev().get_value(ev().OUTPUT_DIRECTORY)
err_dir = ev().get_value(ev().ERROR_DIRECTORY)

def get_git_commit():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').replace('\n','')

def setup():
    if not os.path.exists(input_dir):
        os.mkdir(input_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if not os.path.exists(err_dir):
        os.mkdir(err_dir)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version=f"Version {get_git_commit()}",
                        help='Show the program version')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='info, error, warning, all')
    parser.add_argument('-l', '--debug', action='store_true', help='Starts the program with debug logging enabled')
    parser.add_argument('-m', '--model', default='sm', const='sm', nargs='?', choices=['sm', 'md', 'lg'],
                        help='Specify which model the program should use (default: %(default)s)')
    return parser


def parse_args(args, parser):
    return parser.parse_args(args)


if __name__ == "__main__":
    if input_dir is not None and \
       output_dir is not None and \
       err_dir is not None:
        raise ReferenceError(f'in:{input_dir} out:{output_dir} err:{err_dir}')
    elif input_dir.endswith(('/', '\\')) \
       and output_dir.endswith(('/', '\\')) \
       and err_dir.endswith(('/', '\\')):
        raise TypeError(f'Expected directory but got a file. in:{input_dir} out:{output_dir} err:{err_dir}')

    parser = create_parser()
    parserArgs = parse_args(sys.argv[1:], parser)
    setup()
    process_existing(input_dir)

    start_watch_directory(input_dir)

    print('Exiting...')
