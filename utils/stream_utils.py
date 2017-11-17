# -*- coding: utf8 -*-
from __future__ import unicode_literals

# 本地上传的文件读到内存中
import urllib2
from cStringIO import StringIO
from io import BytesIO
# from PIL import Image


# 网上的文件url读到内存中
def get_io_from_url(url):
    r = urllib2.urlopen(url)
    io = StringIO(r.read())
    io.seek(0)
    return io


# # 网上的图片读到PIL的类中
# def get_pil_im_from_url(original_image_url):
#     r = urllib2.urlopen(original_image_url)
#     io = BytesIO(r.read())
#     io.seek(0)
#     im = Image.open(io)


# 文件流大小
def get_io_size(io):
    io.seek(0, 2)
    file_size = io.tell()
    io.seek(0)
    return file_size


if __name__ == '__main__':
    with open('./log_utils.py', 'rb') as f:
        io = StringIO(f.read())
        print get_io_size(io)