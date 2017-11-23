# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, request, render_template, url_for, jsonify
from flask_login import login_required, current_user

from models.user_models import User
from utils.regex_utils import regex_username, regex_password
from permissions import admin_permission

instance = Blueprint('admin_user', __name__)


@instance.before_request
@login_required
@admin_permission.require(403)
def before_request():
    pass


@instance.route('/admin/user', methods=['GET', 'POST'])
def index():
    return render_template('admin/user.html')