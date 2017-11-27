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


def html_basic_clean(html):
    if not html:
        return html
    replaces = [
        # style=\"font-size: 16px;\", style=\"font-size:14px;font-family:宋体;color:#333333\"
        (r'style="(?:;?font[^:;"]*:[^";]*;?)*"', ''),
        (r'font-(?:size|family):[^;"]*;?', ''),
        (r'&nbsp;', ' '),
        (r'\u200b', ''),
        (r'</?o:p>', ''),  # <o:p></o:p>
        (r'(<span[^>]*)lang="[^"]*"', r'\1'),  # <span lang=\"EN-US\">
        (r'(<table[^>]*)align="[l|r][^"]*"', r'\1'),  # <table align="left|right"> 过滤 align="left"或者align="right"
        (r'data-bind[\s]*=[\s]*"[^"]+"', ''),  # 过滤data-bind标签
        (r'<(/)?st1:[^>]*>', ''),  # 过滤<st1:country-region>标签
    ]
    for reg, rep in replaces:
        html = re.sub(reg, rep, html)
    return html.strip()
