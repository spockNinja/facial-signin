"""
    Some common utility functions used all over the place.
"""

import ConfigParser
import cv2
import os
import stasm
from mailshake import AmazonSESMailer

ROOT = os.path.join(os.path.dirname(__file__), os.pardir)
LOG_DIR = os.path.join(ROOT, 'logs')

_loggers = {}

CONFIG = ConfigParser.ConfigParser()
CONFIG.read(os.path.join(ROOT, 'app.cfg'))


def analyze_photo(photo_path):
    """ Returns facial information about a photo. """
    # Now have opencv read the tempfile into it's img array
    cv_img = cv2.imread(photo_path)
    gray_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    landmarks = stasm.search_single(gray_img)

    # TODO
    # * normalize points to account for differing facial distances
    # * label landmarks
    info = {'eye_distance': '', 'eye_width': '', 'nose_width': ''}  # ... etc
    return info


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


@log('email')
def send_mail(to, subject, text, html=None):
    ''' Utility to handle the Amazon SES mailer and configuration logic.
        If mail isn't enabled, emails are logged instead. '''
    if type(to) != list:
        to = [to]

    mail_access_key = CONFIG.get('email', 'access_key_id')
    mail_access_secret = CONFIG.get('email', 'secret_access_key')
    sender = CONFIG.get('email', 'sender')

    if all([mail_access_key, mail_access_secret, sender]):
        mailer = AmazonSESMailer(mail_access_key, mail_access_secret)
        mailer.send(subject=subject, text=text, html=html,
                    from_email=sender, to=to)


def uuid():
    from uuid import uuid4
    return str(uuid4())
