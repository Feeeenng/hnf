# -*- coding: utf8 -*-
from __future__ import unicode_literals
import os
import glob

from werkzeug.routing import BaseConverter

from flask import Flask
from flask_cache import Cache
from flask_login import LoginManager
from flask_principal import Principal
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

from configs.config import conf
from models.user_models import User
from utils.jinjia_env_utils import generate_csrf_token, embed_html
from scripts import JOBS


cache = Cache()
login_manager = LoginManager()
# login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = '用户需要登录后方可访问该页面'
login_manager.login_message_category = 'warning'
principal = Principal()
scheduler = APScheduler()
sql_db = SQLAlchemy()
socketio = SocketIO()


@login_manager.user_loader
def load_user(uid):
    return User.objects.with_id(uid)


class RegexConverter(BaseConverter):
    """
    添加url正则表达式判断方式
    用法@instance.route('/<regex("\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+"):email>')
    """
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


def __config_blueprints(app):
    dir = os.path.dirname(__file__)
    views_dir = os.path.join(dir, 'controllers')
    views_files = glob.glob(os.path.join(views_dir, '*.py'))
    for views_file in views_files:
        basename = os.path.basename(views_file)
        if basename == '__init__.py':
            continue

        views_file_name = basename[:basename.rindex('.')]
        module = __import__('controllers.{0}'.format(views_file_name), fromlist=['instance'])
        if not hasattr(module, 'instance'):
            continue

        instance = getattr(module, 'instance')
        app.register_blueprint(instance)


def create_app():
    app = Flask(__name__)
    # 读配置文件
    app.config.from_object(conf)

    # 装载定时脚本
    app.config['JOBS'] = JOBS
    app.config['SCHEDULER_VIEWS_ENABLED'] = True

    # flask扩展
    cache.init_app(app, config={'CACHE_TYPE': conf.CACHE_TYPE, 'CACHE_REDIS_URL': conf.CACHE_REDIS_URL})
    login_manager.init_app(app)
    principal.init_app(app)
    sql_db.init_app(app)
    scheduler.init_app(app)
    socketio.init_app(app)
    scheduler.start()

    # 防跨站式攻击
    app.jinja_env.globals['csrf_token'] = generate_csrf_token

    # 模板内嵌html
    app.jinja_env.globals['embed_html'] = embed_html

    # 添加正则url匹配转换器
    app.url_map.converters['regex'] = RegexConverter

    # 蓝图注册
    __config_blueprints(app)

    return app