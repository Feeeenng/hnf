# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from mq.tasks.celery_tasks import func1, func2
from mq.tasks.user_tasks import func3, func4


if __name__ == '__main__':
    res = func1(3, 5)
    print res, res.ready(), res.get(timeout=1), res.traceback

    res = func2(3, 5)
    print res, res.ready(), res.get(timeout=1), res.traceback

    res = func3(2, 5)
    print res, res.ready(), res.get(timeout=1), res.traceback

    res = func4()
    print res, res.ready(), res.get(timeout=1), res.traceback