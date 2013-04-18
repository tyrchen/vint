# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import json
from urlparse import urljoin
import requests

__author__ = 'tchen'
logger = logging.getLogger(__name__)

DEFAULT_HOSTNAME = 'http://exam.tchen.me'
#DEFAULT_HOSTNAME = 'http://localhost:8000'


class Request(object):
    hostname = ''
    api_path = '/'

    def __init__(self, authcode):
        self.authcode = authcode
        self.api_base = self.hostname + self.api_path

    def retrieve(self, id):
        url = urljoin(self.api_base, str(id)) + '/'

        try:
            r = requests.get(url, data={'authcode': self.authcode})
            return json.loads(r.text)
        except:
            return {}

    def delete(self, id):
        url = urljoin(self.api_base, str(id)) + '/'

        try:
            r = requests.delete(url, data={'authcode': self.authcode})
            if r.status_code == requests.codes.no_content:
                return True
            return False
        except:
            return False


class Cerf(object):
    def __init__(self, id, authcode, hostname=DEFAULT_HOSTNAME):
        from misc import config
        self.id = id
        self.authcode = authcode
        self.hostname = hostname
        if config:
            try:
                self.hostname = config.get('global', 'host')
            except:
                pass

        self.interview = Interview(authcode, id)
        self.exam = Exam(authcode)
        self.answer = Answer(authcode)


class Interview(Request):
    hostname = DEFAULT_HOSTNAME
    api_path = '/api/interviews/'

    def __init__(self, authcode, id):
        super(Interview, self).__init__(authcode)
        self.id = id

    def update(self, action, id=None, authcode=None):
        id = id or self.id
        authcode = authcode or self.authcode
        url = urljoin(self.api_base, str(id)) + '/'

        try:
            r = requests.put(url, data={'authcode': authcode, 'action': action})
            return json.loads(r.text)
        except:
            return {}

    def start(self, id=None, authcode=None):
        return self.update('start', id, authcode)

    def finish(self, id=None, authcode=None):
        return self.update('finish', id, authcode)

    def reset(self, id=None, authcode=None):
        return self.update('reset', id, authcode)


class Exam(Request):
    hostname = DEFAULT_HOSTNAME
    api_path = '/api/exams/'


class Answer(Request):
    hostname = DEFAULT_HOSTNAME
    api_path = '/api/answers/'

    def create(self, data):
        headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        try:
            r = requests.post(self.api_base + '?authcode=%s' % self.authcode, data=json.dumps(data), headers=headers)
            if r.status_code != requests.codes.created:
                return {}
            return json.loads(r.text)
        except Exception as ex:
            return {}

