# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mq.tasks import mq_task
from mq.celery_worker import celery_app
from models.user_models import User


@mq_task()
@celery_app.task
def func3(x, y):
    return x ** y


@mq_task()
@celery_app.task
def func4():
    return [u.nickname for u in User.objects(deleted_at=None)]