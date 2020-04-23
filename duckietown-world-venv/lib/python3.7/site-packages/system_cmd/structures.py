from __future__ import unicode_literals
from .utils import indent

__all__ = [
    'CmdResult', 
    'CmdException',
] 

class CmdResult(object):
    def __init__(self, cwd, cmd, ret, rets, interrupted, stdout, stderr):
        self.cwd = cwd
        self.cmd = cmd
        self.ret = ret
        self.rets = rets
        self.stdout = stdout
        self.stderr = stderr
        self.interrupted = interrupted

    def __str__(self):
        from system_cmd.utils import copyable_cmd
        msg = ('The command: %s\n'
               '     in dir: %s\n' % (copyable_cmd(self.cmd), self.cwd))

        if self.interrupted:
            msg += 'Was interrupted by the user\n'
        else:
            msg += 'returned: %s' % self.ret
        if self.rets is not None:
            msg += '\n' + indent(self.rets, 'error>')
        if self.stdout:
            msg += '\n' + indent(self.stdout, 'stdout>')
        if self.stderr:
            msg += '\n' + indent(self.stderr, 'stderr>')
        return msg

    
class CmdException(Exception):
    def __init__(self, cmd_result):
        Exception.__init__(self, str(cmd_result))
        self.res = cmd_result

