#!/usr/bin/env python
from environment.EnvironmentConstants import EnvironmentVariables as ev
ev()
from turtleParser.turtleParser import RuntimeOntology as ro
ro()
import argparse
import os
import sys
import subprocess
from loader.FileLoader import start_watch_directory, process_existing, TripleExtractor
import platform
import knox_util
import spacy
from knox_util import print


assert platform.python_version_tuple()[1] == '8', 'This script requires python 3.8.x in order to run properly'


input_dir = ev.instance.get_value(ev.instance.INPUT_DIRECTORY)
output_dir = ev.instance.get_value(ev.instance.OUTPUT_DIRECTORY)
err_dir = ev.instance.get_value(ev.instance.ERROR_DIRECTORY)
spaCy_model_label = "lg"

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
    parser.add_argument('-m', '--model', default='lg', const='lg', dest='model', nargs='?', choices=['sm', 'md', 'lg', 'cstm'],
                        help='Specify which model the program should use (default: %(default)s)')
    return parser


def parse_args(args, parser):
    return parser.parse_args(args)

# Main matter of the script

if __name__ == "__main__":
    
    parser = create_parser()
    parserArgs = parse_args(sys.argv[1:], parser)
    spaCy_model_label = parserArgs.model
    spaCy_model = f'da_core_news_{spaCy_model_label}'
    knox_util.parserArgs = parserArgs
    print(f'Model argument <{spaCy_model_label}> received from argument parser', 'debug')
    print(f'Loading spaCy model...')
    TripleExtractor.nlp = spacy.load(spaCy_model)
    print(f'Model <{spaCy_model}> loaded!')

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
    process_existing(input_dir, output_dir, err_dir)

    start_watch_directory(input_dir)

    print('Exiting...')
