# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import request
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed

from app import create_app, socketio


# manager配置
hnf = create_app()


@hnf.before_request
def before_request():
    """每个请求前都执行"""
    pass


@hnf.teardown_request
def teardown_request(exception):
    """每个请求结束时都执行"""
    pass


# 当用户登陆的时候，对用户的identity进行判断
@identity_loaded.connect_via(hnf)
def on_identity_loaded(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role))

    # if hasattr(current_user, 'posts'):
    #     for post in current_user.posts:
    #         identity.provides.add(EditBlogPostNeed(unicode(post.id)))


@socketio.on("my error event")
def on_my_event(data):
    raise RuntimeError()


@socketio.on_error_default
def default_error_handler(e):
    print request.event["message"]  # "my error event"
    print request.event["args"]  # (data,)


if __name__ == '__main__':
    socketio.run(hnf)
