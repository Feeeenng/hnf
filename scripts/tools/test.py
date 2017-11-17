# -*- coding: utf8 -*-
from __future__ import unicode_literals
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models.user_models import User


def run():
    for u in User.objects(deleted_at=None):
        print u.id, u.nickname