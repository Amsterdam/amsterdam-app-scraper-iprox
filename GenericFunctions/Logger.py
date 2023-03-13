""" Convenience class for logging facility
"""
import logging
import os


class Logger:
    """ Central logging system. If the environment DEBUG is set, all logging will be printed to the console else it will
        use the operating-system its logging facility.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.debug_enabled = os.getenv('DEBUG', 'false').lower() == 'true'

    def info(self, record):
        """ Log level INFO """
        if self.debug_enabled is True:
            print(record, flush=True)
        else:
            self.logger.info(record)

    def error(self, record):
        """ Log level ERROR """
        if self.debug_enabled is True:
            print(record, flush=True)
        else:
            self.logger.error(record)

    def debug(self, record):
        """ Log level DEBUG """
        if self.debug_enabled is True:
            print(record, flush=True)
        else:
            self.logger.debug(record)
