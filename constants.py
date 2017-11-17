# -*- coding: utf8 -*-
from __future__ import unicode_literals


# 性别
MALE = 'male'
FEMALE = 'female'
GENDERS = (
    (MALE, '男'),
    (FEMALE, '女')
)
GENDERS_DICT = dict(GENDERS)

# 上传文件格式设置
ALLOWED_FORMATS = ['jpg', 'png', 'jpeg']

# 上传文件大小上线
ALLOWED_MAX_SIZE = 2 * 1024 ** 2  # 10M

