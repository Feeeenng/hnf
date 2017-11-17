# -*- coding: utf-8 -*-

import hashlib


class MD5:
    def __init__(self, content):
        self.content = content
        self.md5_content = hashlib.md5(content).hexdigest()

    def get_md5_content(self):
        return self.md5_content

    def compare(self, cmp_content):
        return True if cmp_content == self.md5_content else False

    def add_salt(self, salt):
        return hashlib.md5(self.content + salt).hexdigest()