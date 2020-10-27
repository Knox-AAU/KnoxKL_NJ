#!/usr/bin/python3
import argparse
import logging.config
import logging
import knox_util
import os
import sys
import subprocess
from environment.EnvironmentConstants import EnvironmentVariables as ev
from multiprocessing import Process
from loader.FileLoader import start_watch_directory, process_existing
import platform
import knox_util
from knox_util import print


assert platform.python_version_tuple(
)[1] == '8', 'This script requires python 3.8.x in order to run properly'


input_dir = ev().get_value(ev().INPUT_DIRECTORY)
output_dir = ev().get_value(ev().OUTPUT_DIRECTORY)
err_dir = ev().get_value(ev().ERROR_DIRECTORY)


def get_git_commit():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').replace('\n', '')


def setup():
    print(f'Running setup for input, output, and error dirctories')
    print(f'Checking if {input_dir} exists.', 'debug')
    if not os.path.exists(input_dir):
        print(f'{input_dir} did not exist. Creating it.', 'warning')
        os.mkdir(input_dir)
    print(f'Checking if {output_dir} exists.', 'debug')
    if not os.path.exists(output_dir):
        print(f'{output_dir} did not exist. Creating it.', 'warning')
        os.mkdir(output_dir)
    print(f'Checking if {err_dir} exists.', 'debug')
    if not os.path.exists(err_dir):
        print(f'{err_dir} did not exist. Creating it.', 'warning')
        os.mkdir(err_dir)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version=f"Version {get_git_commit()}",
                        help='Show the program version')
    parser.add_argument('-v', '--verbose', default='info', const='info', dest='verb', nargs='?', choices=[
                        'off', 'quiet', 'info', 'info-only', 'warning', 'error', 'debug'], help='Sets the verbosity level of the printed output')
    parser.add_argument('-l', '--debug', action='store_true',
                        help='Starts the program with debug logging enabled')
    parser.add_argument('-m', '--model', default='sm', const='sm', dest='model', nargs='?', choices=['sm', 'md', 'lg'],
                        help='Specify which model the program should use (default: %(default)s)')
    return parser


def parse_args(args, parser):
    return parser.parse_args(args)

parser = create_parser()
parserArgs = parse_args(sys.argv[1:], parser)
knox_util.parserArgs = parserArgs

# Main matter of the script

if __name__ == "__main__":
    if input_dir is None or \
       output_dir is None or \
       err_dir is None:
        raise ReferenceError(f'in:{input_dir} out:{output_dir} err:{err_dir}')
    elif not input_dir.endswith(('/', '\\')) \
            or not output_dir.endswith(('/', '\\')) \
            or not err_dir.endswith(('/', '\\')):
        raise TypeError(
            f'Expected directory but got a file. in:{input_dir} out:{output_dir} err:{err_dir}')
    setup()
    process_existing(input_dir)

    start_watch_directory(input_dir)

    print('Exiting...')
