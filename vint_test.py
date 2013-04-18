#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
    vint start <id>
    vint finish

Options:
    -h, --help
"""

from vint import vint
from docopt import docopt

arguments = docopt(__doc__)
vint.main(arguments)