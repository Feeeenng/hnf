# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, request, render_template, session, current_app, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from flask_principal import identity_changed, AnonymousIdentity, Identity, RoleNeed, UserNeed, ActionNeed

from models.user_models import User
from utils.regex_utils import regex_username, regex_password
from permissions import ADMIN

instance = Blueprint('admin_auth', __name__)


@instance.before_request
def before_request():
    pass


@instance.route('/admin/login', methods=['GET', 'POST'])
def login():
    """
    登录

    :param: username  账号
    :param: password  密码
    :return:
    """

    if request.method == 'GET':
        return render_template('admin/login.html')

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    code, msg = check_login_params(username, password)
    if not code:
        return jsonify(success=False, error=msg)

    user = User.get_user_by_username(username)
    if not user:
        return jsonify(success=False, error='账户或密码不正确')

    if not user.validate_password(password):
        return jsonify(success=False, error='账户或密码不正确')

    if ADMIN not in user.roles:
        return jsonify(success=False, error='账户或密码不正确')

    login_user(user, True)  # 登录
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))  # 发送信号，载入用户权限
    return jsonify(success=True, url=request.args.get('next') or url_for('admin.index'))


def check_login_params(username, password):
    """
    检查注册参数

    :param: username  账号
    :param: password  密码
    :return:
    """

    if not regex_username(username):
        return False, '账号是6-20位字母或者数字'

    if not regex_password(password):
        return False, '密码是8-16位字母和数字的组合'

    return True, None