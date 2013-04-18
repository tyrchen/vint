#!/usr/bin/env python
# coding: utf-8

import os
import sys
import re

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

setup(
    name='vint',
    version=get_version(),
    description='Cerf exam service client to let the applicant to start/finish the exam',
    long_description=open('README.md').read(),
    license=open("LICENSE.txt").read(),
    author="Tyr Chen",
    author_email="tyr.chen@gmail.com",
    url='https://github.com/tyrchen/vint/',
    keywords="python cerf exam",
    packages=['vint'],
    scripts=['scripts/vint'],
    install_requires=['requests', 'docopt', 'python-dateutil'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',]
)
