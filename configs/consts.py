# -*- coding: utf8 -*-
from __future__ import unicode_literals

# 性别
SECRET = 'secret'
MALE = 'male'
FEMALE = 'female'
GENDERS = (
    (SECRET, 'Secret'),
    (MALE, 'Male'),
    (FEMALE, 'Female')
)
GENDERS_DICT = dict(GENDERS)

# 上传文件格式设置
ALLOWED_FORMATS = ['jpg', 'png', 'jpeg']

# 上传文件大小上线
ALLOWED_MAX_SIZE = 2 * 1024 ** 2  # 10M
