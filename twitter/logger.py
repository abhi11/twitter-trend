import os
from datetime import datetime
'''
Intended to be used as the logging system for operations.
Will help Debug and Test

Logger takes two args for initializing.
first is name of the script that is logging(i.e client of the logger)
second is the name of the log file.

Logging can be used when the API is used by an application to keep track
of what's happening and debugging purposes.
'''

class Logger():

    def __init__(self, logging_client, filename):
        '''
        Initialises the name of client logging .
        This should be the name of the script using the logger.
        '''
        self._file = "/var/log/electrichut/electrichut.log"
        self._name = logging_client
        if filename:
            self._file = filename

    def log(self, msg, mode="INFO"):
        '''
        logs the msg, default mode is INFO
        '''
        handle = open(self._file, "a+")
        cur_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        log_msg = "[%s]:%s %s %s\n" % (mode, self._name, cur_time, msg)
        handle.write(log_msg)

    def debug(self, msg):
        '''
        logs in DEBUG mode
        '''
        self.log(msg, "DEBUG")

    def info(self, msg):
        '''
        logs in INFO mode
        '''
        self.log(msg, "INFO")

    def warning(self, msg):
        '''
        logs in WARN mode
        '''
        self.log(msg, "WARN")

    def error(self, msg):
        '''
        logs ERROR, could used inside the except blocks
        '''
        self.log(msg, "ERROR")
