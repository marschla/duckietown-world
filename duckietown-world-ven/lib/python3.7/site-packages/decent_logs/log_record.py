# -*- coding: utf-8 -*-
__all__ = ['LogRecord']

class LogRecord(object):
    
    def __init__(self, name, timestamp, string, level):
        self.name = name
        self.timestamp = timestamp
        self.string = string
        self.level = level
    
        levels = ['info', 'error', 'debug', 'warn']
        if not level in levels:
            msg = 'Got %r, expected %r.' % (level, levels)
            raise ValueError(msg)
        
    def __str__(self):
        return '%s: %s' % (self.name, self.string)
        
    def write_to_logger(self, logger):
        s = self.__str__()
        level = self.level
        if level == 'info':
            logger.info(s)
        elif level == 'error':
            logger.error(s)
        elif level == 'debug':
            logger.debug(s)
        elif level == 'warn':
            logger.warn(s)
        else:
            assert False
