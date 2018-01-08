# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask_socketio import send, emit, join_room, leave_room
from app import socketio
from events import authenticated_only


@socketio.on('typing')
def handle_my_custom_event(message):
    emit('typing', message, broadcast=True)


@socketio.on('my event')
def handle_my_custom_event(json):
    emit('response', json['data'], broadcast=True)


@socketio.on('send_message')
def send_message(message):
    emit('response', '\n' + message, broadcast=True)


# 加入房间
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)


# 离开房间
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)