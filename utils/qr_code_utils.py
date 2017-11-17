# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from cStringIO import StringIO
import base64

import qrcode


def generate_qrcode(data, version=None, error_correction=None, box_size=None, border=None):
    qr = qrcode.QRCode(
        # version值为1~40的整数,控制二维码的大小,(最小值是1,是个12*12的矩阵)
        # 如果想让程序自动确定,将值设置为 None 并使用 fit 参数即可
        version=version,
        # error_correction: 控制二维码的错误纠正功能,可取值下列4个常量
        #   ERROR_CORRECT_L: 大约7%或更少的错误能被纠正
        #   ERROR_CORRECT_M(默认): 大约15%或更少的错误能被纠正
        #   ERROR_CORRECT_Q: 大约25%或更少的错误能被纠正
        #   ERROR_CORRECT_H: 大约30%或更少的错误能被纠正
        error_correction=error_correction or qrcode.constants.ERROR_CORRECT_M,
        # 控制二维码中每个小格子包含的像素数
        box_size=box_size or 6,
        # 控制边框(二维码与图片边界的距离)包含的格子数(默认为4,是相关标准规定的最小值)
        border=border or 4,
    )

    # 将vCard数据填入qr
    qr.add_data(data)

    qr.make(fit=True)

    # 生成图片
    img = qr.make_image()

    img_io = StringIO()

    # 将图片存入指定路径文件
    img.save(img_io, 'png')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.read())
    img_io.close()
    return img_base64


# img_base64 = generate_qrcode('http://www.baidu.com')
# <img src="data:image/png;base64,{{ img_io }}">
