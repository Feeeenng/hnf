# -*- coding: utf8 -*-
from __future__ import unicode_literals
import re


def regex_email(email):
    """
    邮箱验证

    :param email:
    :return:
    """

    p = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
    match = re.match(p, email)
    if match:
        return True
    return False


def regex_nickname(nickname):
    """
    昵称的正则，规则：中文，英文字母或者数字，长度要在1到10位

    :param nickname:
    :return:
    """

    p = re.compile(r'^[\u4e00-\u9fa5a-zA-Z0-9]{1,10}$')
    if re.match(p, nickname):
        return True
    return False


def regex_password(password):
    """
    密码的正则，规则：必须是数字和英文字母的组合，长度要在6到20位

    :param password:
    :return:
    """

    p = re.compile(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z_]{6,20}$')
    if re.match(p, password):
        return True
    return False


def regex_username(username):
    """
    账号的正则，规则：英文字母或者数字，长度要在6到20位

    :param username:
    :return:
    """

    p = re.compile(r'^\w{6,20}$')
    if re.match(p, username):
        return True
    return False


def get_request_path_key_word(request_path):
    p = re.compile(r'\/(\w+)')
    return re.findall(p, request_path)