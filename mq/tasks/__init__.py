# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import wraps
from mq.celery_worker import celery_config


def mq_task(queue=celery_config.CELERY_DEFAULT_QUEUE):
    def _decorate(func):
        @wraps(func)
        def __decorate(*args, **kwargs):
            if queue not in celery_config.queue_name_list:
                raise Exception('queue not in [{0}]'.format(', '.join(celery_config.queue_name_list)))
            return func.apply_async(args=args, kwargs=kwargs, queue=queue)
        return __decorate
    return _decorate