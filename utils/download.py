from contextlib import contextmanager
import os
import tempfile
from fabric import operations

@contextmanager
def download(remote_path):
    temp_path = tempfile.mktemp()
    local = operations.get(remote_path, temp_path)
    try:
        yield local[0]
    finally:
        os.remove(temp_path)