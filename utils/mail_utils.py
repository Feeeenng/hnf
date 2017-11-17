# -*- coding: utf8 -*-
from __future__ import unicode_literals

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import time
from threading import Thread


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


class Email(object):
    def __init__(self, sender, receivers, subject, mails_cc=None, mails_bcc=None, body=None, html=None,
                 smtp_sever='localhost', username=None, password=None):
        self.__sender = sender
        self.__receivers = receivers
        self.__mails_cc = mails_cc
        self.__mails_bcc = mails_bcc
        self.__subject = subject
        self.__body = body
        self.__html = html
        self.__date = time.time()
        self.__smtp_sever = smtp_sever
        self.__username = username
        self.__password = password
        self.__message = MIMEMultipart()

    def build_email(self):
        self.__message['From'] = self.__sender
        self.__message['To'] = ';'.join(list(set(self.__receivers)))
        self.__message['Subject'] = Header(self.__subject, 'utf-8')
        self.__message['Cc'] = ';'.join(set(self.__mails_cc or []) - set(self.__receivers))
        self.__message['Bcc'] = ';'.join(set(self.__mails_bcc or []) - set(self.__receivers) - set(self.__mails_cc or []))
        if self.__body:
            self.__message.attach(MIMEText(self.__body, 'plain', 'utf-8'))
        if self.__html:
            self.__message.attach(MIMEText(self.__html, 'html', 'utf-8'))

    def add_attachment(self, io, filename, content_type='application/octet-stream'):
        att = MIMEText(io.getvalue(), 'base64', 'utf-8')
        att["Content-Type"] = content_type
        att["Content-Disposition"] = 'attachment; filename="{0}"'.format(filename)
        self.__message.attach(att)
        io.seek(0)

    @async
    def send_email(self):
        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.__smtp_sever)
            if self.__username and self.__password:
                smtp.login(self.__username, self.__password)
            smtp.sendmail(self.__sender, list(set(self.__receivers) | set(self.__mails_cc or []) | set(self.__mails_bcc or [])), self.__message.as_string())
            smtp.close()
        except smtplib.SMTPException, ex:
            print ex


# sender = 'from@mocal.cn'
# receivers = ['369685930@qq.com']
# subject = '测试邮箱'
# mails_cc = ['nengfang.han@17zuoye.com']
# mails_bcc = ['haner27@126.com']
# body = '测试邮箱'
#
# from cStringIO import StringIO
# with open('hello.txt') as f:
#     io = StringIO(f.read())
#     io.seek(0)
#
# email = Email(sender=sender, receivers=receivers, subject=subject, mails_cc=mails_cc, mails_bcc=mails_bcc)
# email.build_email()
# email.add_attachment(io, 'llll.txt')
# email.send_email()