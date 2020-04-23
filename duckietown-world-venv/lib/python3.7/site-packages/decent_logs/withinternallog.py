# -*- coding: utf-8 -*-
from .log_record import LogRecord
from contracts import contract
from decent_logs import logger
import time
 

__all__ = ['WithInternalLog']


class WithInternalLog(object):
    """ 
        Subclassing this class gives the object the capability
        of calling self.info, self.error, etc. and have their
        logging memorized.
    """
        
    def _init_log(self):
        self.log_lines = []  # log records
        self.children = {}    
        name = self.__class__.__name__  # don't call str() yet
        self._log_name = name
        self.set_log_output(True)
        
    def _wil_check_inited(self):
        """ Make sure that we inititalized the log system.
            We don't count on a constructor being called. """
        if not 'children' in self.__dict__:
            self._init_log()
        
    @contract(name='str')
    def set_name_for_log(self, name):
        self._wil_check_inited()
        self._log_name = name
        
        # update its names
        for id_child, child in self.children.items():
            its_name = self._log_name + ':' + id_child
            child.set_name_for_log(its_name)

    @contract(id_child='str|None')
    def log_add_child(self, id_child, child):
        self._wil_check_inited()
        if not isinstance(child, WithInternalLog):
            msg = 'Tried to add child of type %r' % type(child)
            self.error(msg)
            raise ValueError(msg)
        if id_child is None:
            id_child = type(child).__name__
        
        if child in self.children.values():
            old_id = self.log_child_name(child)
            del self.children[old_id]
            if id_child is None:
                id_child = old_id
        
        while id_child in self.children:
            #self.warn('Invalid name %s  ' % id_child)
            id_child += 'b'

        self.children[id_child] = child
        its_name = self._log_name + ':' + id_child
        child.set_name_for_log(its_name)

    def log_child_name(self, child):
        """ Rrturns the id under which the child was registered. """
        for id_child, x in self.children.items():
            if x == child:
                return id_child
        raise ValueError('No such child %r.' % child)
 
    
    @contract(enable='bool')
    def set_log_output(self, enable):
        self._wil_check_inited()
        """ 
            Enable or disable instantaneous on-screen logging.
            If disabled, things are still memorized.     
        """
        self.log_output_enabled = enable
    
    def _save_and_write(self, s, level):
        status = type(self).__name__
        if status is None:
            status = ''
        else:
            status = ' (%s): ' % status
            #status = ' (%s#%s): ' % (status, id(self))

        string = status + s
        name = self._log_name
        record = LogRecord(name=name,
                           timestamp=time.time(),
                           string=string,
                           level=level)
        self.log_lines.append(record)
        if self.log_output_enabled:
            record.write_to_logger(logger)
        
    @contract(s='str')
    def info(self, s):
        """ Logs a string; saves it for visualization. """
        self._wil_check_inited()
        self._save_and_write(s, 'info')
        
    @contract(s='str')
    def debug(self, s):
        self._wil_check_inited()
        self._save_and_write(s, 'debug')
    
    @contract(s='str')
    def error(self, s):
        self._wil_check_inited()
        self._save_and_write(s, 'error')

    @contract(s='str')
    def warn(self, s):
        self._wil_check_inited()
        self._save_and_write(s, 'warn')
    
    def get_log_lines(self):
        """ Returns a list of LogRecords """
        self._wil_check_inited()
        lines = list(self.log_lines)
        for child in self.children.values():
            lines.extend(child.get_log_lines())
        lines.sort(key=lambda x: x.timestamp)
        return lines
    
    def get_raw_log_lines(self):
        """ Returns a list of strings """
        self._wil_check_inited()
        raw = map(LogRecord.__str__, self.get_log_lines())
        return raw
