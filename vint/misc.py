# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from dateutil import parser
from datetime import datetime

__author__ = 'tchen'
logger = logging.getLogger(__name__)


def calc_time_spent(start):
    started = parser.parse(start)
    now = datetime.now()
    diff = now - started
    return diff / 60