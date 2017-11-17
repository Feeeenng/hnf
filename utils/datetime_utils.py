# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
import time
import pytz

__author__ = 'longlong.yu'


"""
    时间相关工具
"""

# inner cache
_local_tz = pytz.timezone('Asia/Shanghai')
_utc_tz = pytz.utc


def local_timezone():
    """返回本地时区"""
    return _local_tz


def utc_timezone():
    """返回utc时区"""
    return _utc_tz


def get_tzname(dt):
    """获取时区名字"""
    if not dt or not dt.tzinfo:
        return None
    return getattr(dt.tzinfo, 'zone', None) or dt.tzinfo.tzname(dt)


def to_utc_time(dt):
    """本地时间变为utc时间"""
    if not dt:
        return dt
    if dt and dt.tzinfo:
        tzname = get_tzname(dt)
        if tzname == _utc_tz.zone:
            return dt
        if tzname == _local_tz.zone:
            return _utc_tz.localize(dt.replace(tzinfo=None) - timedelta(hours=8))

    raise Exception('unrecognised timezone {}'.format(dt.tzinfo or 'null'))


def to_local_time(dt):
    """utc时间变为本地时间"""
    if not dt:
        return dt
    if dt.tzinfo:
        tzname = get_tzname(dt)
        if tzname == _local_tz.zone:
            return dt
        if tzname == _utc_tz.zone:
            return _local_tz.localize(dt.replace(tzinfo=None) + timedelta(hours=8))
    raise Exception('unrecognised timezone {}'.format(dt.tzinfo or 'null'))


def now_lambda():
    """返回utc当前时间"""
    return _utc_tz.localize(datetime.utcnow())


def utc_now():
    """返回utc当前时间"""
    return _utc_tz.localize(datetime.utcnow())


def local_now():
    """返回当前本地时间"""
    return _local_tz.localize(datetime.now())


def to_timestamp(dt):
    """
    时间戳, 秒
    """
    return int(time.mktime(dt.timetuple()))


def current_year(utc=False):
    """
        utc: False 按当前时区，True 按UTC
    """
    now = now_lambda()
    return now.year if utc else to_local_time(now).year


def format_datetime(dt, format='%Y-%m-%d %H:%M:%S', utc=False):
    """
        utc: False 按当前时区显示，True 按UTC显示
    """
    if not dt:
        return ''
    if get_tzname(dt) not in (_local_tz.zone, _utc_tz.zone):
        raise Exception('unrecognised timezone {}'.format(dt.tzinfo or 'null'))

    dt = to_utc_time(dt) if utc else to_local_time(dt)
    return dt.strftime(format)


def to_datetime(dt_str, format='%Y-%m-%d %H:%M:%S', utc=False):
    """
        utc: False 按当前时区解析，True 按UTC解析
    """
    # noinspection PyBroadException
    try:
        dt = datetime.strptime(dt_str, format)
        return _utc_tz.localize(dt) if utc else _local_tz.localize(dt)
    except:
        return None


def combine_datetime(dt, time):
    """使用dt中的日期和time返回新的datetime"""
    if get_tzname(dt) not in (_local_tz.zone, _utc_tz.zone):
        raise Exception('unrecognised timezone {}'.format(dt.tzinfo or 'null'))
    return dt.tzinfo.localize(datetime.combine(dt, time))


def get_datetime(*args, **kwargs):
    """返回datetime并指定时区"""
    return (_utc_tz if kwargs.get('utc', False) else _local_tz).localize(datetime(*args, **kwargs))


def gt(dt1, dt2, delta=None):
    """
    dt1是否大于dt2, 且差值大于delta
    :param dt1:
    :param dt2:
    :param delta: 时间的差值
    :return: True or False
    """
    if not delta:
        return dt1 > dt2
    return (dt1 - delta) > dt2


def gte(dt1, dt2, delta=None):
    """
    dt1是否大于dt2, 且差值大于等于delta
    :param dt1:
    :param dt2:
    :param delta: 时间的差值
    :return: True or False
    """
    if not delta:
        return dt1 >= dt2
    return (dt1 - delta) >= dt2
