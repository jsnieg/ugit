import hashlib
import os

from typing import Literal

GIT_DIR : Literal['str'] = '.ugit'

def init() -> None:
    try:
        os.makedirs(GIT_DIR)
        os.makedirs(f'{GIT_DIR}/objects')
    except OSError:
        print('Target directory already exists.')
        return

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