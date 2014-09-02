"""
    Some common utility functions used all over the place.
"""

import ConfigParser
import os

ROOT = os.path.join(os.path.dirname(__file__), os.pardir)
LOG_DIR = os.path.join(ROOT, 'logs')

_loggers = {}

CONFIG = ConfigParser.ConfigParser()
CONFIG.read(os.path.join(ROOT, 'app.cfg'))


def create_log(log_name):
    """Returns a logger instance that writes to the passed log_name file.

    @param log_name: File name for the log file. Stored at ../log/
    """
    import logging
    import logging.handlers

    logfile = os.path.join(LOG_DIR, log_name + '.log')
    try:
        if not os.path.exists(logfile):
            open(logfile, 'w').close()
            os.chmod(logfile, 0o664)
    except IOError:
        # We are passing here because if the file can't be written
        # we will log to stdout
        pass

    # Gets a new instance of logger with the log_name
    logger = logging.getLogger(log_name)
    handler = logging.handlers.TimedRotatingFileHandler(logfile,
                                                        when='midnight')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(message)s')
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


def log(logfile='log'):
    """ A decorator that logs when a function is called
        and keeps track of it's arguments.
        You can specify a log file, otherwise it will just go to
        logs/log """

    logger = create_log(logfile)

    def log_wrap(func):
        def inner_log(*args, **kwargs):
            logger.info('{0} called with {1} - {2}'.format(func.__name__,
                                                           str(args),
                                                           str(kwargs)))
            try:
                return func(*args, **kwargs)
            except:
                logger.warning('Error in ' + func.__name__, exc_info=1)

        return inner_log

    return log_wrap


def resp(success=True, message=''):
    """ Helper function to return a response dict"""
    return {'success': success, 'message': message}


def uuid():
    from uuid import uuid4
    return str(uuid4())
