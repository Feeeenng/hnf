# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask_login import UserMixin
from mongoengine import StringField, ListField, IntField, DateTimeField, EmailField, EmbeddedDocument, \
    EmbeddedDocumentField, FloatField

from . import BaseDocument, register_pre_save, conf
from models.user_models import User
from utils.datetime_utils import format_datetime, now_lambda


@register_pre_save()
class ChatRoom(BaseDocument):  # 房间表
    name = StringField()  # 房间名
    desc = StringField()  # 房间描述
    creator_id = StringField()  # 创建人
    members = IntField(default=0)  # 成员数

    meta = {
        'collection': 'chat_room',
        'db_alias': conf.DATABASE_NAME,
        'strict': False
    }

    @classmethod
    def join_room(cls, room_id, user_id):
        rur = RoomUserRef.objects(room_id=room_id, user_id=user_id, deleted_at=None).first()
        if not rur:
            now = now_lambda()
            rur = RoomUserRef(room_id=room_id, user_id=user_id)  # 创建关系
            rur.histories.append(EmbeddedStatus(status=rur.status, operated_at=now))
            rur.save()
            cls.objects(id=room_id, deleted_at=None).update(inc__members=1)  # 人数加1

    @classmethod
    def leave_room(cls, room_id, user_id):
        rur = RoomUserRef.objects(room_id=room_id, user_id=user_id, deleted_at=None).first()
        if rur:
            now = now_lambda()
            rur.status = rur.LEFT
            rur.histories.append(EmbeddedStatus(status=rur.status, operated_at=now))
            rur.save()
            cls.objects(room_id=room_id, deleted_at=None).update(inc__members=-1)  # 人数减1

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'creator_id': self.creator_id,
            'creator': User.get_username(self.creator_id),
            'created_at': format_datetime(self.created_at, '%Y-%m-%d'),
            'members': self.members
        }


class EmbeddedStatus(EmbeddedDocument):
    status = IntField()
    operated_at = DateTimeField()


@register_pre_save()
class RoomUserRef(BaseDocument):  # 房间和用户关系表
    JOINED = 1
    LEFT = 2
    STATUS = [
        (JOINED, '加入'),
        (LEFT, '离开')
    ]
    STATUS_DICT = dict(STATUS)

    room_id = StringField()  # 房间ID
    user_id = StringField()  # 用户ID
    status = IntField(choices=STATUS, default=JOINED)  # 当前关系
    histories = ListField(EmbeddedDocumentField(EmbeddedStatus), default=[])

    meta = {
        'collection': 'room_user_ref',
        'db_alias': conf.DATABASE_NAME,
        'strict': False
    }

    @classmethod
    def get_members(cls, room_id, status):
        return cls.objects(room_id=room_id, status=status, deleted_at=None).count()

    def as_dict(self, with_history=False):
        dic = {
            'room_id': self.room_id,
            'user_id': self.user_id,
            'status': self.status,
            'status_text': self.STATUS_DICT.get(self.status, '-')
        }

        if with_history:
            histories = []
            for history in self.histories:
                histories.append({
                    'status': history.status,
                    'status_text': self.STATUS_DICT.get(history.status, '-'),
                    'operated_at': format_datetime(history.operated_at, '%Y-%m-%d')
                })
            dic.update(histories=histories)

        return dic