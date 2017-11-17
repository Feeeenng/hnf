# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user

from . import access_condition, memoize

instance = Blueprint('index', __name__)


@instance.before_request
def before_request():
    pass


@instance.route('/', methods=['GET'])
@access_condition(1, 3)
@login_required
def index():
    return render_template('index.html')