# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask_socketio import emit, join_room, leave_room
from app import socketio
from events import authenticated_only
from utils.datetime_utils import now_lambda, format_datetime


@socketio.on('join', namespace='/chat')
@authenticated_only
def join(data):
    uid = data['uid']
    group_id = data['group_id']
    now = now_lambda()
    now_str = format_datetime(now)
    join_room(group_id)
    # todo: 加群数据逻辑
    emit('status', {}, room=group_id)


@socketio.on('text', namespace='/chat')
@authenticated_only
def text(data):
    uid = data['uid']
    group_id = data['group_id']
    msg = data['msg']
    now = now_lambda()
    now_str = format_datetime(now)
    # todo: 数据存储逻辑
    emit('message', {}, room=group_id)


@socketio.on('leave', namespace='/chat')
@authenticated_only
def leave(data):
    uid = data['uid']
    group_id = data['group_id']
    now = now_lambda()
    now_str = format_datetime(now)
    leave_room(group_id)
    # todo: 退群数据逻辑
    emit('status', {}, room=group_id)