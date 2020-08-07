# -*- coding: utf-8 -*-

''' Logging module for MComix. Provides a logger 'mcomix' with a few
pre-configured settings. Functions in this module are redirected to
this default logger. '''

import logging
import sys
import locale
from logging import DEBUG, INFO, WARNING, ERROR

from mcomix import i18n

__all__ = ['debug', 'info', 'warning', 'error', 'setLevel',
           'DEBUG', 'INFO', 'WARNING', 'ERROR']

levels = {
    'all': DEBUG,
    'debug': DEBUG,
    'info': INFO,
    'warn': WARNING,
    'error': ERROR,
}


class PrintHandler(logging.Handler):
    ''' Handler using L{print} to output messages. '''

    def __init__(self):
        super(PrintHandler, self).__init__()

    def emit(self, record):
        print(i18n.to_unicode(self.format(record)))


# Set up default logger.
__logger = logging.getLogger('mcomix')
__logger.setLevel(WARNING)
if not __logger.hasHandlers():
    __handler = PrintHandler()
    __handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(threadName)s] %(levelname)s: %(message)s',
        '%H:%M:%S'))
    __logger.addHandler(__handler)

# The following functions direct all input to __logger.

debug = __logger.debug
info = __logger.info
warning = __logger.warning
error = __logger.error
setLevel = __logger.setLevel


# vim: expandtab:sw=4:ts=4
