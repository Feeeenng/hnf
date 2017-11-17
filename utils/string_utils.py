# -*- coding: utf8 -*-
from __future__ import unicode_literals
import re
from datetime import datetime
from random import randint


def camel_to_underscore_line(name):
    s = ''
    for i, c in enumerate(name):
        if c.isupper():
            s += '_{0}'.format(c.lower())
        else:
            s += c

    if s.startswith('_'):
        s = s[1:]
    return s


def get_upper_letters(s):
    m = ''
    for c in s:
        if c.isupper():
            m += c

    return m


def get_unique_name(ext):
    now = datetime.now()
    return '{0}{1}.{2}'.format(now.strftime('%Y%m%d%H%M%S'), randint(100, 999), ext)

