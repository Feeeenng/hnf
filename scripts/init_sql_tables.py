# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from manage import hnf
from sql_models import create_tables


if __name__ == '__main__':
    with hnf.app_context():
        create_tables()
