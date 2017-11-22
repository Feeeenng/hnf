# -*- coding: utf8 -*-
from flask import Blueprint, render_template, request, url_for, g
from flask_login import current_user
from utils.regex_utils import get_request_path_key_word
from permissions import ADMIN

instance = Blueprint('error', __name__)


def get_source(path, user):
    """
    返回页面判断：
    ***
    1.登录状态下，admin权限的账号访问后台的url，返回后台的root页；访问前台的url，返回前台的root页
    2.登录状态下，非admin权限的账号不管访问前台还是后台，统统返回前台的root页面
    3.非登录状态下，如果访问后台的url就返回后台的root页，访问前台的url就返回前台的root页

    :param path:
    :return:
    """

    kws = get_request_path_key_word(path)
    if user.is_authenticated:
        if ADMIN in user.roles:
            if 'admin' in kws:
                return url_for('admin.index')
            else:
                return url_for('index.index')
        return url_for('index.index')

    else:
        if 'admin' in kws:
            return url_for('admin.index')
        return url_for('index.index')


# emergency handler
@instance.app_errorhandler(403)
def forbidden(e):
    source = get_source(request.path, current_user)
    return render_template('error/403.html', source=source), 403


@instance.app_errorhandler(404)
def page_not_found(e):
    source = get_source(request.path, current_user)
    return render_template('error/404.html', source=source), 404


@instance.app_errorhandler(500)
def internal_server_error(e):
    source = get_source(request.path, current_user)
    return render_template('error/500.html', source=source), 500
