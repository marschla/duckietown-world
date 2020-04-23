from __future__ import unicode_literals
import six

from contracts import contract


def cmd2args(s):
    ''' if s is a list, leave it like that; otherwise split()'''
    if isinstance(s, list):
        return s
    elif isinstance(s, six.string_types):
        return s.split()
    else:
        assert False


def wrap(header, s, N=30):
    header = '  ' + header + '  '
    l1 = '-' * N + header + '-' * N
    l2 = '-' * N + '-' * len(header) + '-' * N
    return l1 + '\n' + s + '\n' + l2


def result_format(cwd, cmd, ret, stdout=None, stderr=None):
    msg = ('Command:\n\t{cmd}\n'
           'in directory:\n\t{cwd}\nfailed with error {ret}').format(
            cwd=cwd, cmd=cmd, ret=ret
    )
    if stdout is not None:
        msg += '\n' + wrap('stdout', stdout)
    if stderr is not None:
        msg += '\n' + wrap('stderr', stderr)
    return msg


def indent(s, prefix):
    lines = s.split('\n')
    lines = ['%s%s' % (prefix, line.rstrip()) for line in lines]
    return '\n'.join(lines)


# @contract(cmds='list(string)')
def copyable_cmd(cmds):
    """ Returns the commands as a copyable string. """

    # @contract(x='string')
    def copyable(x):
        if (not ' ' in x) and (not '"' in x) and (not '"' in x):
            return x
        else:
            if '"' in x:
                return "'%s'" % x
            else:
                return '"%s"' % x

    return " ".join(map(copyable, cmds))
