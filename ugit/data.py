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

def hash_object(data) -> str:
    """
    """
    # Create a hash of the content of a file using SHA-1
    oid: str = hashlib.sha1(data).hexdigest()
    # Store the file under a related hash
    with open(f'{GIT_DIR}/objects/{oid}', 'wb') as out:
        out.write(data)
    return oid

def get_object(oid: str) -> bytes:
    with open(f'{GIT_DIR}/objects/{oid}', 'rb') as f:
        return f.read()