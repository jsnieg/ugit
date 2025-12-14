# data.py -> Manages the data in .ugit directory. Here will be the code that actually touches files on-disk.

import hashlib
import os

from typing import Generator, Any
from typing import Literal
from collections import namedtuple

GIT_DIR : Literal['str'] = '.ugit'

def init() -> None:
    """
    Initialises a .ugit directory for empty repository as specified by GIT_DIR above.\n
    """
    try:
        
        # Similar to mkdir but makedirs throws OSError if directory exists.
        os.makedirs(GIT_DIR)
        os.makedirs(f'{GIT_DIR}/objects')
    except OSError:
        print('Target directory already exists.')
        return

RefValue = namedtuple('RefValue', ['symoblic', 'value'])

def update_ref(ref, value) -> None:
    assert not value.symbolic
    ref_path: str = f'{GIT_DIR}/{ref}'
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    with open(ref_path, 'w') as f:
        f.write(value.value)

def get_ref(ref) -> str | None:
    ref_path = f'{GIT_DIR}/{ref}'
    value = None
    if os.path.isfile(ref_path):
        with open(ref_path) as f:
            value: str = f.read().strip()
        
    if value and value.startswith('ref:'):
        return get_ref(value.split(':', 1)[1].strip())
        
    return RefValue(symbolic=False, value=value)
    
def iter_refs() -> Generator[Any, Any, Any]:
    # iter_refs is a generator iterating on all available refs
    # it will return HEAD from the ugit root directory
    # and everything under .ugit/refs.
    # _ here is a throwoaway variable, only root and filenames are required
    refs = ['HEAD']
    for root, _, filenames in os.walk(f'{GIT_DIR}/refs/'):
        root = os.path.relpath(root, GIT_DIR)
        refs.extend(f'{root}/{name}' for name in filenames)
    for refname in refs:
        yield refname, get_ref(refname)

def hash_object(data, type_='blob') -> str:
    """
    Hashes the object to allow it be unique.
    """
    obj = type_.encode() + b'\x00' + data
    # Create a hash of the content of a file using SHA-1
    oid: str = hashlib.sha1(obj).hexdigest()
    # Store the file under a related hash
    with open(f'{GIT_DIR}/objects/{oid}', 'wb') as out:
        out.write(obj)
    return oid

def get_object(oid: str, expected='blob') -> bytes:
    """
    Return object of the repository created.
    """
    with open(f'{GIT_DIR}/objects/{oid}', 'rb') as f:
        obj: bytes = f.read()
    
    # Types bytes
    type_, _, content = obj.partition(b'\x00')
    type_: str = type_.decode()

    if expected is not None:
        assert type_ == expected, f'Expected {expected}, got {type_}'
    return content