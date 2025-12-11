#https://www.leshenko.net/p/ugit/#

# Imports
import argparse
import os
import subprocess
import sys
import textwrap


# Local
from . import base
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

    oid: str = base.get_oid

    # Create a new 'init' command
    init_parser = commands.add_parser('init')
    # Assign function to it
    init_parser.set_defaults(func=init)

    hash_object_parser = commands.add_parser('hash-object')
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument('file')

    cat_file_parser = commands.add_parser('cat-file')
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument('object', type=oid)

    write_tree_parser = commands.add_parser('write-tree')
    write_tree_parser.set_defaults(func=write_tree)

    read_tree_parser = commands.add_parser('read-tree')
    read_tree_parser.set_defaults(func=read_tree)
    read_tree_parser.add_argument('tree', type=oid)

    commit_parser = commands.add_parser('commit')
    commit_parser.set_defaults(func=commit)
    commit_parser.add_argument('-m', '--message', required=True)

    log_parser = commands.add_parser('log')
    log_parser.set_defaults(func=log)
    log_parser.add_argument('oid', default='@', type=oid, nargs='?')

    checkout_parser = commands.add_parser('checkout')
    checkout_parser.set_defaults(func=checkout)
    checkout_parser.add_argument('oid', type=oid)

    tag_parser = commands.add_parser('tag')
    tag_parser.set_defaults(func=tag)
    tag_parser.add_argument('name')
    tag_parser.add_argument('oid', default='@', type=oid, nargs='?')

    branch_parser = commands.add_parser('branch')
    branch_parser.set_defaults(func=branch)
    branch_parser.add_argument('name')
    branch_parser.add_argument('start_point', default='@', type=oid, nargs='?')

    k_parser = commands.add_parser('k')
    k_parser.set_defaults(func=k)

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
    sys.stdout.buffer.write(data.get_object(args.object, expected=None))

def write_tree(args):
    print(base.write_tree())

def read_tree(args):
    base.read_tree(args.tree)

def commit(args):
    print(base.commit(args.message))

def log(args):
    for oid in base.iter_commits_and_parents({args.oid}):
        commit = base.get_commit(oid)

        print(f'commit {oid}\n')
        print(textwrap.indent(commit.message, '    '))
        print('')

def checkout(args):
    base.checkout(args.oid)

def tag(args):
    base.create_tag(args.name, args.oid)

def branch(args) -> None:
    base.create_branch(args.name, args.start_point)
    print(f'Branc {args.name} created at {args.start_point[:10]}')

def k(args) -> None:
    """
    Similar function to gitk which is a graphical visualization tool for Git.

    Usage: ugit k

    reference: (#k: Print refs, Render graph)
    """
    dot = 'digraph commits {\n'
    oids = set()
    # iter_refs is a generator iterating on all available  refs
    # it will return HEAD from the ugit root directory
    # and everything under .ugit/refs.
    for refName, ref in data.iter_refs():
        dot += f'"{refName}" [shape=note]\n'
        dot += f'"{refName}" -> "{ref}"\n'
        oids.add(ref)

    for oid in base.iter_commits_and_parents(oids):
        commit = base.get_commit(oid)
        dot += f'"{oid}" [shape=box style=filled label={oid[:10]}]\n'
        if commit.parent:
            dot += f'"{oid}" -> "{commit.parent}"\n'
            
    dot += '}'
    print(dot)

    with subprocess.Popen(
        ['dot', '-Tgtk', '/dev/stdin'],
        stdin=subprocess.PIPE) as proc:
        proc.communicate (dot.encode())