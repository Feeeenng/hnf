# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from functools import wraps
from flask_login import current_user
from flask_socketio import disconnect


def authenticated_only(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped