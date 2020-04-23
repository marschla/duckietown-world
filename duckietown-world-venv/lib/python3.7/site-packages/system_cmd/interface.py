from __future__ import unicode_literals
from .meat import system_cmd_result

__all__ = [
    'system_cmd_show', 
    'system_cmd', 
    'system_run',
]

def system_cmd_show(cwd, cmd): 
    ''' Display command, raise exception. '''
    system_cmd_result(
            cwd, cmd,
            display_stdout=True,
            display_stderr=True,
            raise_on_error=True)
        
def system_cmd(cwd, cmd):
    ''' Do not output; return value. '''
    res = system_cmd_result(
            cwd, cmd,
            display_stdout=False,
            display_stderr=False,
            raise_on_error=False)
    return res.ret

def system_run(cwd, cmd):
    ''' Gets the stdout of a command,  raise exception if it failes '''
    res = system_cmd_result(
            cwd, cmd,
            display_stdout=False,
            display_stderr=False,
            raise_on_error=True)
    return res.stdout
