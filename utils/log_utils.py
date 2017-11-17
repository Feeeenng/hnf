# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from logging import Logger, Formatter, INFO, StreamHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, SMTPHandler


class MineLog(Logger):
    def __init__(self, name, log_path=None, level=INFO, log_format=None, date_format=None):
        # 初始化父类
        super(MineLog, self).__init__(name, level)

        # 设置文件路径
        if log_path is None:
            log_path = os.path.join(os.path.dirname(__file__), '{0}.log'.format(name))
        self.log_path = log_path

        # 设置日志格式和时间格式
        if log_format is None:
            log_format = '[%(name)s][%(asctime)s][%(levelname)s]%(message)s -- %(filename)s line:%(lineno)d'

        if date_format is None:
            date_format = '%Y-%m-%d %H:%M:%S'

        self.formatter = Formatter(log_format, date_format)

        # 添加标准输出handler和时间轮流输出文件中
        for handler in [self.stream_handler(), self.timed_rotating_handler()]:
            self.addHandler(handler)

    def stream_handler(self):
        handler = StreamHandler()
        handler.setLevel(self.level)
        handler.setFormatter(self.formatter)
        return handler

    def rotating_handler(self, level=None, max_bytes=10*1024*1024, backup_count=5):
        handler = RotatingFileHandler(self.log_path, maxBytes=max_bytes, backupCount=backup_count)
        handler.setLevel(self.level if level is None else level)
        handler.setFormatter(self.formatter)
        return handler

    def timed_rotating_handler(self, level=None, when='D', interval=1, backup_count=5):
        handler = TimedRotatingFileHandler(self.log_path, when, interval, backup_count)
        handler.setLevel(self.level if level is None else level)
        handler.setFormatter(self.formatter)
        return handler

    def smtp_handler(self, level=None):
        handler = SMTPHandler(('smtp.126.com', 25), 'sender@126.com', ['eaxmple@qq.com'], 'Test SMTPHandler',
                              ('username', 'password'))
        handler.setLevel(self.level if level is None else level)
        handler.setFormatter(self.formatter)
        return handler


if __name__ == '__main__':
    ml = MineLog('http')
    ml.info('wo shi dafei')