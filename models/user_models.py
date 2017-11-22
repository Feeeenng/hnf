# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask_login import UserMixin
from mongoengine import StringField, ListField, IntField, DateTimeField, EmailField, EmbeddedDocument, \
    EmbeddedDocumentField, FloatField

from . import BaseDocument, register_pre_save, conf
from constants import GENDERS, GENDERS_DICT
from permissions import ROLES, MEMBER
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

    @classmethod
    def register(cls, username, password, nickname, email, gender):
        user = cls()
        user.username = username
        user.password = MD5(password, salt=conf.SECRET_KEY).md5_content
        user.nickname = nickname
        user.email = email
        user.gender = gender
        user.roles = [MEMBER]
        user.save()

    def validate_password(self, password):
        return MD5(password, salt=conf.SECRET_KEY).equal(self.password)

    def as_dict(self):
        dic = dict(self.to_mongo())
        dic['gender_text'] = GENDERS_DICT.get(self.gender, '')

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

