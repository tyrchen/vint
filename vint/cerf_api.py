# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from datetime import datetime
from dateutil import parser
import json
from urlparse import urljoin
import requests

__author__ = 'tchen'
logger = logging.getLogger(__name__)

DEFAULT_HOSTNAME = 'http://exam.tchen.me'


class Cerf(object):
    def __init__(self, id, authcode, hostname=DEFAULT_HOSTNAME):
        self.id = id
        self.authcode = authcode
        self.hostname = hostname
        self.interview = Interview(id, authcode, hostname)
        self.exam = Exam(authcode, hostname)
        self.answer = Answer(authcode, hostname)


class Interview(object):
    def __init__(self, id, authcode, hostname=DEFAULT_HOSTNAME):
        self.id = id
        self.authcode = authcode
        self.api_base = hostname + '/api/interviews/'

    def retrieve(self, id=None, authcode=None):
        id = id or self.id
        authcode = authcode or self.authcode
        url = urljoin(self.api_base, id)

        r = requests.get(url, data={'authcode': authcode})
        return json.loads(r.text)

    def update(self, data, id=None, authcode=None):
        id = id or self.id
        authcode = authcode or self.authcode
        url = urljoin(self.api_base, str(id))

        info = {'authcode': authcode}
        info.update(data)

        r = requests.put(url, data=info)
        return json.loads(r.text)

    def start(self, id=None, authcode=None):
        return self.update({'action': 'start'}, id, authcode)

    def finish(self, id=None, authcode=None):
        return self.update({'action': 'finish'}, id, authcode)

    def reset(self, id=None, authcode=None):
        return self.update({'action': 'reset'}, id, authcode)


class Exam(object):
    def __init__(self, authcode, hostname=DEFAULT_HOSTNAME):
        self.authcode = authcode
        self.api_base = hostname + '/api/exams/'

    def retrieve(self, id):
        url = urljoin(self.api_base, str(id))

        r = requests.get(url, data={'authcode': self.authcode})
        return json.loads(r.text)


class Answer(object):
    def __init__(self, authcode, hostname=DEFAULT_HOSTNAME):
        self.authcode = authcode
        self.api_base = hostname + '/api/answers/'

    def create(self, data):
        headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        r = requests.post(self.api_base + '?authcode=%s' % self.authcode, data=json.dumps(data), headers=headers)
        if r.status_code != requests.codes.created:
            return False
        return True
