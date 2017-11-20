# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, request, render_template, session, current_app, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from flask_principal import identity_changed, AnonymousIdentity, Identity, RoleNeed, UserNeed, ActionNeed

from models.user_models import User
from utils.regex_utils import regex_password, regex_email, regex_nickname, regex_username
from utils.token_utils import confirm_token, generate_confirmation_token, generate_captcha
from utils.mail_utils import Email
from utils.datetime_utils import timedelta
from constants import MALE, FEMALE

instance = Blueprint('auth', __name__)


@instance.before_request
def before_request():
    pass


@instance.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录

    :param: username  账号
    :param: password  密码
    :param: remember  记住
    :return:
    """

    if request.method == 'GET':
        return render_template('auth/login.html')

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    remember = request.form.get('remember', False, type=int).strip()

    code, msg = check_login_params(username, password)
    if not code:
        return jsonify(success=False, error=msg)

    user = User.get_user_by_username(username)
    if not user:
        return jsonify(success=False, error='账户或密码不正确')

    if not user.validate_password(password):
        return jsonify(success=False, error='账户或密码不正确')

    login_user(user, remember)  # 登录
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))  # 发送信号，载入用户权限
    return jsonify(success=True, url=request.args.get('next') or url_for('index.index'))


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


@instance.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    注销

    :return:
    """

    for key in ['identity.id', 'identity.auth_type']:
        session.pop(key, None)

    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    current_user.logout()
    return redirect(url_for('index.index'))


@instance.route('/register', methods=['GET', 'POST'])
def register():
    """
    注册

    :param: username  账号
    :param: password  密码
    :param: confirm   重复密码
    :param: email     邮箱
    :param: nickname  昵称
    :param: gender    性别
    :return:
    """

    if request.method == 'GET':
        return render_template('auth/register.html')

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    confirm = request.form.get('confirm', '').strip()
    nickname = request.form.get('nickname', '').strip()
    email = request.form.get('email', '').strip()
    gender = request.form.get('gender', '').strip()

    code, msg = check_register_params(username, password, confirm, nickname, email, gender)
    if not code:
        return jsonify(success=False, error=msg)

    user = User(username=username, password=password, nickname=nickname, email=email, gender=gender)
    user.save()
    return jsonify(success=True)


def check_register_params(username, password, confirm, nickname, email, gender):
    """
    检查注册参数

    :param: username  账号
    :param: password  密码
    :param: confirm   重复密码
    :param: email     邮箱
    :param: nickname  昵称
    :param: gender    性别
    :return:
    """

    if not regex_username(username):
        return False, '账号是6-20位字母或者数字'

    user = User.get_user_by_username(username)
    if user:
        return False, '账户【{0}】已存在'.format(username)

    if not regex_password(password):
        return False, '密码是6-20位字母和数字的组合'

    if password != confirm:
        return False, '两次输入的密码不一致'

    if not regex_nickname(nickname):
        return False, '昵称是1-10位中文、字母或者数字'

    user = User.get_user_by_nickname(nickname)
    if user:
        return False, '昵称【{0}】已存在'.format(nickname)

    if not regex_email(email):
        return False, '邮箱格式不正确'

    user = User.get_user_by_email(email)
    if user:
        return False, '邮箱【{0}】已被使用'.format(email)

    if gender not in [MALE, FEMALE]:
        return False, '请选择性别'

    return True, None

