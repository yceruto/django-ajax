#!/usr/bin/env python

import os
import sys

cmds = [
    'python runtests_decorator.py',
]

for cmd in cmds:
    retval = os.system(cmd)
    if retval:
        sys.exit(1)
