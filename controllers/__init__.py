# -*- coding: utf8 -*-
from __future__ import unicode_literals
from functools import wraps
import time

from flask import jsonify, request
from app import cache
from models import redis

# 缓存方法
memoize = cache.memoize  # 用于缓存结果，以函数名以及参数进行缓存
cached = cache.cached  # 用于缓存视图函数，以request.path进行缓存


class TimeoutError(Exception):
    def __init__(self, value):
        self.value = value


def retry(attempts=3, interval=5):
    def _decorate(func):
        @wraps(func)
        def __decorate(*args, **kwargs):
            for attempt in xrange(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt >= attempts:
                        print '重复次执行{0}次失败'.format(attempt)
                    else:
                        print '第{0}次执行失败，{1}s后继续开始第{2}次尝试, error msg:{3}'.format(attempt, interval, attempt + 1, e)
                        time.sleep(interval)
        return __decorate
    return _decorate


def access_condition(times=10, limit=3):
    def decorate(func):
        @wraps(func)
        def _decorate(*args, **kwargs):
            now = int(time.time())
            ip = request.remote_addr

            key = 'acc_{0}_{1}'.format(ip, func.__name__)
            if not redis.get(key):
                redis.setex(key, [], 10)

            v = redis.get(key)
            v = eval(v)

            v.append(now)
            d_time = now - times
            over_list = filter(lambda a: a >= d_time, v)
            redis.setex(key, over_list, 10)

            if len(over_list) - 1 >= limit:
                return jsonify(success=False, error='请求过于频繁哦，小伙！')
            return func(*args, **kwargs)
        return _decorate
    return decorate