# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, request, render_template, session, current_app, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from permissions import admin_permission


instance = Blueprint('admin', __name__)


@instance.before_request
@login_required
@admin_permission.require(403)
def before_request():
    pass


@instance.route('/admin', methods=['GET', 'POST'])
def index():
    return render_template('admin/index.html')