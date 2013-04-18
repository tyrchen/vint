# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import os
from dateutil import parser
from datetime import datetime


__author__ = 'tchen'
logger = logging.getLogger(__name__)


def calc_time_spent(start):
    started = parser.parse(start)
    now = datetime.now()
    diff = now - started
    return diff.seconds / 60


def get_config():
    from os.path import expanduser
    import ConfigParser
    config = ConfigParser.ConfigParser()
    filename = expanduser('~/.vintconfig')
    if os.path.exists(filename):
        config.readfp(open(filename))
        return config
    else:
        return None

config = get_config()