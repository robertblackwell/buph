import sys
import pathlib
import logging
import logging.handlers
from loguru import logger as guru_logger
# look into https://github.com/Delgan/loguru
# @TODO fix the timezone

def config_log_guru():
    logpath = pathlib.WindowsPath(pathlib.WindowsPath.home(), "buph_logs", "buph_{time}.log")
    guru_logger.add(str(logpath), retention = "2 days")
    return guru_logger

def config_logger():
# Change root logger level from WARNING (default) to NOTSET in order for all messages to be delegated.
    logging.getLogger().setLevel(logging.NOTSET)

    # Add stdout handler, with level INFO
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    formater = logging.Formatter('%(name)-13s: %(levelname)-8s %(message)s', datefmt="%m/%d/%Y %I:%M:%S %p %Z")
    console.setFormatter(formater)
    logging.getLogger().addHandler(console)

    # Add file rotating handler, with level DEBUG
    rotatingHandler = logging.handlers.RotatingFileHandler(filename='c:\\Users\lightroom\\bulogs\\bu.log', maxBytes=10000, backupCount=5)
    rotatingHandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt="%m/%d/%Y %I:%M:%S %p %Z")
    rotatingHandler.setFormatter(formatter)
    logging.getLogger().addHandler(rotatingHandler)

    log = logging.getLogger("app." + __name__)

    log.debug('Debug message, should only appear in the file.')
    log.info('Info message, should appear in file and stdout.')
    log.warning('Warning message, should appear in file and stdout.')
    log.error('Error message, should appear in file and stdout.')

    return log
if False:
    buph_logger = config_logger()
else:
    buph_logger = config_log_guru()