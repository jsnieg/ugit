#https://www.leshenko.net/p/ugit/#

import argparse

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

    return parser.parse_args()

def init(args) -> None:
    """
    """
    print('Hello, World!')