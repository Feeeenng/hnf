# -*- coding: utf8 -*-
from __future__ import unicode_literals
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import random


def generate_confirmation_token(secret_key, key, data, expiration=86400):
    s = Serializer(secret_key, expires_in=expiration)
    return s.dumps({key: data})


def confirm_token(secret_key, token):
    s = Serializer(secret_key)
    try:
        d = s.loads(token)
    except:
        return False, None
    # if d.get(key) != data:
    #     return False
    return True, d


def generate_captcha():
    return ''.join([str(random.choice(xrange(10))) for i in xrange(6)])