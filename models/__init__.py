# -*- coding: utf8 -*-
from __future__ import unicode_literals
from utils.datetime_utils import now_lambda
import random

from mongoengine import signals, connect, Document, StringField, DateTimeField
from redis import Redis

from utils.string_utils import get_upper_letters
from configs.config import conf


def create_document_id(class_name, id_prefix=None):
    remain_str = '{0}{1}'.format(now_lambda().strftime('%Y%m%d%H%M%S'), str(random.randint(100, 999)))
    if id_prefix:
        id = '{0}{1}'.format(id_prefix.upper(), remain_str)
    else:
        name = get_upper_letters(class_name)
        id = '{0}{1}'.format(name, remain_str)
    return id


def register_pre_save(id_prefix=None):
    def _decorate(clazz):
        if id_prefix:
            clazz.id_prefix = id_prefix
        signals.pre_save.connect(clazz.pre_save, sender=clazz)
        return clazz
    return _decorate


class BaseDocument(Document):
    id = StringField(primary_key=True)
    created_at = DateTimeField(default=None)
    updated_at = DateTimeField(default=None)
    deleted_at = DateTimeField(default=None)

    meta = {
        'abstract': True,
        'strict': False
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document._created = True
        if not document.id:
            id_prefix = None
            if hasattr(cls, 'id_prefix'):
                id_prefix = getattr(cls, 'id_prefix')

            document.id = create_document_id(cls.__name__, id_prefix)
            document.created_at = now_lambda()
        document.updated_at = now_lambda() if document.id and document.updated_at else document.created_at


# mongo数据库初始化
conn = connect(conf.DATABASE_NAME,
               alias=conf.DATABASE_NAME,
               host=conf.DATABASE_HOST,
               port=conf.DATABASE_PORT,
               username=conf.DATABASE_USERNAME,
               password=conf.DATABASE_PASSWORD,
               tz_aware=True)

db = conn[conf.DATABASE_NAME]

# redis初始化
redis = Redis(
    host=conf.REDIS_HOST,
    port=conf.REDIS_PORT,
    db=conf.REDIS_DB,
    socket_connect_timeout=3,
    socket_timeout=3)