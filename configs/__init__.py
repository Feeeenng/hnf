# -*- coding: utf8 -*-
from __future__ import unicode_literals

from utils.datetime_utils import timedelta


class Config(object):
    SECRET_KEY = 'h!a@n#n$e%n^g&f*a(n)g'

    # cookie时长， 超时关闭浏览器忘记
    REMEMBER_COOKIE_DURATION = timedelta(seconds=3600 * 12)

    # session， 超过时长会话删除
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=3600 * 12)

    # 加密salt
    SALT = '*^)h#a&n@#$;.'

    @classmethod
    def is_production(cls):
        return cls.STAGE == 'production'

    @classmethod
    def is_development(cls):
        return cls.STAGE == 'development'


class ProductionConfig(Config):
    STAGE = 'production'
    DEBUG = False

    # mongodb 链接信息
    DATABASE_NAME = 'hnf'
    DATABASE_HOST = '127.0.0.1'
    DATABASE_PORT = 27017
    DATABASE_USERNAME = 'han'
    DATABASE_PASSWORD = 'haner27'
    DATABASE_URL = 'mongodb://{0}:{1}@{2}:{3}'.format(DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST,
                                                      DATABASE_PORT)

    # 缓存 相关信息
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 0
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = '{0}://{1}:{2}/{3}'.format(CACHE_TYPE, REDIS_HOST, REDIS_PORT, REDIS_DB)

    # elasticsearch
    ES_HOST = '127.0.0.1'
    ES_PORT = 9200

    # mysql
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:haner27@127.0.0.1:3306/hnf?charset=utf8'

    # 邮箱配置
    EMAIL_SMTP_SERVER = 'smtp.126.com'
    EMAIL_USERNAME = 'haner27'
    EMAIL_PASSWORD = 'mqhaner27'
    EMAIL_SENDER = 'haner27@126.com'

    # celery配置
    CELERY_BROKER_URL = 'redis://127.0.0.1:5000/1'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:5000/2'


class DevelopmentConfig(Config):
    STAGE = 'development'
    DEBUG = True

    # mongodb 链接信息
    DATABASE_NAME = 'hnf'
    DATABASE_HOST = '127.0.0.1'
    DATABASE_PORT = 27017
    DATABASE_USERNAME = 'han'
    DATABASE_PASSWORD = 'haner27'
    DATABASE_URL = 'mongodb://{0}:{1}@{2}:{3}'.format(DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST,
                                                      DATABASE_PORT)

    # 缓存 相关信息
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 0
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = '{0}://{1}:{2}/{3}'.format(CACHE_TYPE, REDIS_HOST, REDIS_PORT, REDIS_DB)

    # elasticsearch
    ES_HOST = '127.0.0.1'
    ES_PORT = 9200

    # mysql
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:haner27@127.0.0.1:3306/hnf?charset=utf8'

    # 邮箱配置
    EMAIL_SMTP_SERVER = 'smtp.126.com'
    EMAIL_USERNAME = 'haner27'
    EMAIL_PASSWORD = 'mqhaner27'
    EMAIL_SENDER = 'haner27@126.com'

    # celery配置
    CELERY_BROKER_URL = 'redis://127.0.0.1:5000/1'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:5000/2'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}