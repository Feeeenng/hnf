# -*- coding: utf8 -*-
from flask import Blueprint, render_template, request, url_for, g
from utils.regex_utils import get_request_path_key_word

instance = Blueprint('error', __name__)


# emergency handler
@instance.app_errorhandler(403)
def forbidden(e):
    kws = get_request_path_key_word(request.path)
    if 'admin' in kws:
        source = url_for('admin.index')
    else:
        source = url_for('index.index')
    return render_template('error/403.html', source=source), 403


@instance.app_errorhandler(404)
def page_not_found(e):
    kws = get_request_path_key_word(request.path)
    if 'admin' in kws:
        source = url_for('admin.index')
    else:
        source = url_for('index.index')
    return render_template('error/404.html', source=source), 404


@instance.app_errorhandler(500)
def internal_server_error(e):
    kws = get_request_path_key_word(request.path)
    if 'admin' in kws:
        source = url_for('admin.index')
    else:
        source = url_for('index.index')
    return render_template('error/500.html', source=source), 500
