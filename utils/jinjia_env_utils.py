# -*- coding: utf8 -*-
from __future__ import unicode_literals
from uuid import uuid4

from flask import session, Markup, render_template


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = __some_random_string()
    return session['_csrf_token']


def __some_random_string():
    return unicode(uuid4())


def embed_html(template_name, **kwargs):
    return Markup(render_template(template_name, **kwargs))
