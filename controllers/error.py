# -*- coding: utf8 -*-
from flask import Blueprint, render_template

instance = Blueprint('error', __name__)


# emergency handler
@instance.app_errorhandler(403)
def forbidden(e):
    return render_template('error/403.html'), 403


@instance.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@instance.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500
