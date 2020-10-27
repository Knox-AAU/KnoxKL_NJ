#!/usr/bin/python3
import platform

assert platform.python_version_tuple()[1] == '8', 'This script requires python 3.8.x in order to run properly'

import sys, subprocess, asyncio, os, knox_util, logging, logging.config, argparse

from loader.FileLoader import start_watch_directory, process_existing
from multiprocessing import Process
from environment.EnvironmentConstants import EnvironmentVariables as ev
from inspect import getframeinfo, stack

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
    parser.add_argument('-v', '--verbose', default='info', const='info', dest='verb', nargs='?', choices=['off','info', 'warning', 'error', 'debug'], help='Sets the verbosity level of the printed output')
    parser.add_argument('-l', '--debug', action='store_true', help='Starts the program with debug logging enabled')
    parser.add_argument('-m', '--model', default='sm', const='sm', dest='model', nargs='?', choices=['sm', 'md', 'lg'],
                        help='Specify which model the program should use (default: %(default)s)')
    return parser

def parse_args(args, parser):
    return parser.parse_args(args)

def get_file_debug_info():
    caller = getframeinfo(stack()[2][0])
    return f'{caller.filename}:{caller.lineno} '

parser = create_parser()
parserArgs = parse_args(sys.argv[1:], parser)

if parserArgs.verb != 'off':
    def print_verbose(message: str, level: str):
        label_switcher={
            1: '\033[1;4;31m[ERROR]\033[0;31m',
            2: '\033[1;4;33m[WARNING]\033[0;33m',
            3: '\033[1;4;37m[INFO]\033[0;37m',
            4: '\033[1;4;34m[DEBUG]\033[0;34m'
        }
        level_switcher = {
            'error': 1,
            'warning': 2,
            'info': 3,
            'debug': 4
        }
        log_level = level_switcher.get(parserArgs.verb, 3)
        specified_log_level = level_switcher.get(level, 3)
        file_debug_info = ''
        if specified_log_level <= 2 or specified_log_level == 4:
            file_debug_info = get_file_debug_info()
        if specified_log_level <= log_level:
            print(f'{label_switcher[specified_log_level]} {file_debug_info}{message}\033[0m')
else:
    def print_verbose(message, level='off'):
        print(message)

# Main matter of the script

if __name__ == "__main__":
    if input_dir is None or \
       output_dir is None or \
       err_dir is None:
        raise ReferenceError(f'in:{input_dir} out:{output_dir} err:{err_dir}')
    elif not input_dir.endswith(('/', '\\')) \
       or not output_dir.endswith(('/', '\\')) \
       or not err_dir.endswith(('/', '\\')):
        raise TypeError(f'Expected directory but got a file. in:{input_dir} out:{output_dir} err:{err_dir}')
    print_verbose('Initialising directories', 'error')
    print_verbose('Initialising directories', 'warning')
    print_verbose('Initialising directories', 'info')
    print_verbose('Initialising directories', 'debug')
    setup()
    process_existing(input_dir)

    start_watch_directory(input_dir)

    print('Exiting...')
