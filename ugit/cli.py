#https://www.leshenko.net/p/ugit/#

# Imports
import argparse
import os
import sys

# Local
from . import data

# Misc
from argparse import ArgumentParser

def main() -> None:
    """
    """
    args = parse_args()
    args.func(args)

def parse_args():
    """
    """
    # Parser to pass command string lines to Python object
    parser: ArgumentParser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest='command')
    commands.required = True

    # Create a new 'init' command
    init_parser = commands.add_parser('init')
    # Assign function to it
    init_parser.set_defaults(func=init)

    hash_object_parser = commands.add_parser('hash-object')
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument('file')

    cat_file_parser = commands.add_parser('cat-file')
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument('object')

    return parser.parse_args()

def init(args) -> None:
    """
    """
    data.init()
    print(f'Initialized empty ugit repository in {os.getcwd()}/{data.GIT_DIR}')

def hash_object(args):
    with open(args.file, 'rb') as f:
        print(data.hash_object(f.read()))

def cat_file(args):
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.object))