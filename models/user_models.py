# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import url_for, current_app, render_template
from flask_login import UserMixin, login_user, logout_user
from mongoengine import StringField, ListField, IntField, DateTimeField, EmailField, EmbeddedDocument, \
    EmbeddedDocumentField, FloatField

from . import BaseDocument, register_pre_save, conf
from constants import GENDERS, GENDERS_DICT
from permissions import ROLES, MEMBER
from utils.datetime_utils import now_lambda
from utils.regex_utils import regex_password, regex_email, regex_nickname
from utils.md5_utils import MD5
from utils.mail_utils import Email
from utils.token_utils import generate_confirmation_token, confirm_token
from utils.datetime_utils import format_datetime


@register_pre_save()
class User(UserMixin, BaseDocument):
    username = StringField(required=True)  # 账号
    password = StringField(required=True)  # 密码
    nickname = StringField(required=True)  # 昵称
    email = EmailField(default=None, unique=True)  # 联系邮箱
    gender = StringField(choices=GENDERS)  # 性别
    sign_in_ip = StringField(default=None)  # 登录IP
    sign_in_at = DateTimeField(default=None)  # 登录时间
    sign_out_at = DateTimeField(default=None)  # 注销时间
    roles = ListField(StringField(choices=ROLES, default=MEMBER), default=[])  # 角色
    privileges = ListField(IntField(), default=None)  # 权限

    meta = {
        'collection': 'user',
        'db_alias': conf.DATABASE_NAME,
        'strict': False
    }

    @classmethod
    def get_user_by_username(cls, username):
        return cls.objects(username=username).first()

    @classmethod
    def get_user_by_nickname(cls, nickname):
        return cls.objects(nickname=nickname).first()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.objects(email=email).first()

    def validate_password(self, password):
        return MD5(password, salt=conf.SECRET_KEY).equal(self.password)

    def as_dict(self):
        dic = dict(self.to_mongo())
        dic['gender_text'] = GENDERS_DICT.get(self.gender, '')
        if self.sign_in_ip:
            del dic['sign_in_ip']

        if self.sign_in_at:
            del dic['sign_in_at']

        if self.sign_out_at:
            del dic['sign_out_at']

        if self.roles:
            del dic['with_roles']

        if self.privileges:
            del dic['privileges']

        if self.created_at:
            dic['created_at'] = format_datetime(self.created_at)

        if self.updated_at:
            dic['updated_at'] = format_datetime(self.updated_at)

        if self.deleted_at:
            dic['deleted_at'] = format_datetime(self.deleted_at)

        return dic

