# -*- coding: utf8 -*-
from flask import Blueprint, render_template, request, url_for, jsonify
from flask_login import current_user

from models.chat_models import ChatRoom

instance = Blueprint('chat', __name__)


@instance.route('/chat')
def index():
    return render_template('chat/index.html')


@instance.route('/chat/new_room', methods=['POST'])
def new_room():
    """
    创建房间

    :param: room_name    房间名
    :param: desc         描述
    :return:
    """

    name = request.form.get('room_name', '').strip()
    if not name:
        return jsonify(success=False, error='参数缺失room_name')

    desc = request.form.get('desc', '').strip()
    if not desc:
        return jsonify(success=False, error='参数缺失desc')

    room = ChatRoom(name=name, desc=desc, creator_id=current_user.id)
    room.save()

    ChatRoom.join_room(room.id, current_user.id)
    return jsonify(success=True, room_id=room.id)


@instance.route('/chat/room_list', methods=['POST'])
def room_list():
    """
    房间列表

    :param: page         页码
    :param: room_id      房间ID
    :param: room_name    房间名
    :param: creator_id   创建人
    :param: sort_field   排序字段
    :return:
    """

    page = request.form.get('page', 1, type=int)
    room_id = request.form.get('room_id', '').strip()
    room_name = request.form.get('room_name', '').strip()
    creator_id = request.form.get('creator_id', '').strip()
    sort_field = request.form.get('sort_field', '-created_at').strip()

    query = {
        'deleted_at': None
    }

    if room_name:
        query.update(name__contains=room_name)

    if room_id:
        query.update(id=room_id)

    if creator_id:
        query.update(creator_id=creator_id)

    crs = ChatRoom.objects(**query).order_by(sort_field)
    total = crs.count()
    per_page = 10
    data = map(lambda a: a.as_dict(), crs[(page - 1) * per_page: page * per_page])
    return jsonify(success=True, data=data, total=total, per_page=per_page)