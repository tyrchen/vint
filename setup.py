#!/usr/bin/env python
# coding: utf-8

import os
import sys
import re
import vint

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version():
    VERSIONFILE = 'vint/__init__.py'
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def long_description():
    return '''
    The command line client for cerf exam service.
    '''

setup(
    name='vint',
    version=get_version(),
    description='Cerf exam service client to let the applicant to start/finish the exam',
    long_description=long_description(),
    license=vint.__license__,
    author=vint.__author__,
    author_email=vint.__email__,
    url='http://tchen.me',
    download_url='https://github.com/tyrchen/vint',
    keywords="python cerf exam",
    packages=['vint'],
    scripts=['bin/vint'],
    install_requires=['requests', 'docopt', 'python-dateutil'],
    module='vint',
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7']
)
