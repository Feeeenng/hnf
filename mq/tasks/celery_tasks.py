# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mq.celery_worker import celery_app
from mq.tasks import mq_task, CallbackTask
from time import sleep


@mq_task('common')
@celery_app.task(base=CallbackTask)
def func1(x, y):
    sleep(10)
    return x + y


@mq_task('email')
@celery_app.task(base=CallbackTask)
def func2(x, y):
    return x * y
