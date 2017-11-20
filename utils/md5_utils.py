# -*- coding: utf-8 -*-

import hashlib


class MD5:
    def __init__(self, content, salt=None):
        self.content = content
        self.salt = salt

    @property
    def md5_content(self):
        return hashlib.md5(self.content + self.salt or '').hexdigest()

    def equal(self, cmp_content):
        return cmp_content == self.md5_content
