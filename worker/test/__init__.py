#
# Author: water - waterlzj@gmail.com
#
# Last modified: 2016-11-09 17:59 +0800
#
# Description: module init
#/

import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger
