# -*- coding: utf-8-*-
from __future__ import unicode_literals
import os
import glob
from celery import Celery
from kombu import Exchange, Queue


def get_tasks_module_path_list():
    path_list = []
    mq_work_dir = os.path.dirname(__file__)
    mq_work_dir_name = os.path.basename(mq_work_dir)
    tasks_dir_name = 'tasks'
    for tasks_file in glob.glob(os.path.join(mq_work_dir, tasks_dir_name, '*.py')):
        basename = os.path.basename(tasks_file)
        if basename == '__init__.py':
            continue

        tasks_module_name = basename[:basename.rindex('.')]
        path_list.append('{0}.{1}.{2}'.format(mq_work_dir_name, tasks_dir_name, tasks_module_name))
    return path_list


class CeleryConfig(object):
    BROKER_URL = 'redis://127.0.0.1:6379/3'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/4'

    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'Asia/Beijing'
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
    CELERY_ENABLE_UTC = True

    CELERY_QUEUES = (
        Queue('common', Exchange('common'), routing_key='common', consumer_arguments={'x-priority': 10}),
        Queue('email', Exchange('email'), routing_key='email', consumer_arguments={'x-priority': 5}),
        Queue('file', Exchange('file'), routing_key='file', consumer_arguments={'x-priority': 1})
    )
    CELERY_DEFAULT_QUEUE = 'common'
    CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
    CELERY_DEFAULT_ROUTING_KEY = 'common'

    @property
    def queue_name_list(self):
        return [q.name for q in self.CELERY_QUEUES]


celery_config = CeleryConfig()
celery_app = Celery('hnf', include=get_tasks_module_path_list())
celery_app.config_from_object(celery_config)


if __name__ == '__main__':
    celery_app.start()
