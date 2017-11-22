# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, render_template, jsonify
from sql_models.user_models import User


instance = Blueprint('test', __name__)


@instance.before_request
def before_request():
    pass


@instance.route('/test', methods=['GET'])
def test():
    d = 1 / 0
    return jsonify(success=True, data=d)
