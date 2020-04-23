from __future__ import unicode_literals
from contracts import contract

__all__ = ['find_executable']


@contract(returns="str|None")
def find_executable(program):
    """ Checks if a program exists. Returns None otherwise """

    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None
