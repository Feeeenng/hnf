# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import Image, ImageDraw, ImageFont, ImageFilter
import random
from cStringIO import StringIO
import base64

number = {
    0: ['0', '零'],
    1: ['1', '一', '壹'],
    2: ['2', '二', '贰'],
    3: ['3', '三', '叁'],
    4: ['4', '四', '肆'],
    5: ['5', '五', '伍'],
    6: ['6', '六', '陆'],
    7: ['7', '七', '柒'],
    8: ['8', '八', '捌'],
    9: ['9', '九', '玖'],
}

operate = {
    '+': ['+', '加'],
    '-': ['-', '减'],
    '*': ['*', '乘'],
    '/': ['/', '除']
}


# 随机数字1:
def random_number1(a, b):
    random_num = random.randint(a, b)
    a_number_list = number[random_num]
    return random_num, random.choice(a_number_list)


# 随机数字2：
def random_number2(num_list):
    random_num = random.choice(num_list)
    a_number_list = number[random_num]
    return random_num, random.choice(a_number_list)


# 计算
def calculate(a, b, op):
    if op == '+':
        return a + b

    if op == '-':
        return a - b

    if op == '*':
        return a * b

    if op == '/':
        return a/b


# 随机操作符
def random_operate():
    op = random.choice(['+', '-', '*', '/'])
    return op, random.choice(operate[op])


# 获取操作数2的列表
def get_num2_list(num1, op):
    if op == '+' or op == '*':
        return [i for i in range(0, 10)]

    if op == '-':
        return [i for i in range(0, 10) if i <= num1]

    if op == '/':
        return [i for i in range(1, 10) if num1 % i == 0]


# 随机颜色1:
def rndColor_ganrao():
    color_list = [(255, 255, 255), (0, 0, 0)]
    return random.choice(color_list)


# 随机颜色:
def rndColor():
    color_list = [(255, 106, 106), (40, 144, 255), (0, 64, 128)]  # 粉 蓝 墨绿
    return random.choice(color_list)


# 随机字体
def rndFont():
    font_list = ['static/font/STHUPO.TTF']  # ['/Library/Fonts/华文细黑.ttf', '/Library/Fonts/yuanti.ttc', '/Library/Fonts/Xingkai.ttc']
    return random.choice(font_list)


# 随机字体大小
def rndFontSize():
    return random.randint(20, 30)


# 随机背景颜色
def rndBackGroundColor():
    return random.choice([(237, 247, 255), (247, 254, 236)])


def generate_verify_code():
    # 240 x 40:
    width = 36 * 4  # 验证码图片宽
    height = 40  # 验证码图片高
    image = Image.new('RGB', (width, height), rndBackGroundColor())  # 白底

    # 创建Draw对象:
    draw = ImageDraw.Draw(image)

    # 填充每个像素（加模糊点）:
    # for x in range(width):
    #     for y in range(height):
    #         draw.point((x, y), fill=rndColor_ganrao())

    # 获取随机元素
    color = rndColor()
    font_format = rndFont()
    op_num1_size = rndFontSize()
    op_size = rndFontSize()
    op_num2_size = rndFontSize()

    # 创建Font对象:
    font1 = ImageFont.truetype(font_format, op_num1_size)
    font2 = ImageFont.truetype(font_format, op_size)
    font3 = ImageFont.truetype(font_format, op_num2_size)

    # 输出文字:
    num1, num_str1 = random_number1(0, 9)
    draw.text((40 * 0 + 15, (height - op_num1_size)/2), num_str1, font=font1, fill=color)

    op, op_str = random_operate()
    draw.text((40 * 1 + 15, (height - op_size)/2), op_str, font=font2, fill=color)

    # 根据 操作数1 和 op 确认 操作数2集合
    num2_list = get_num2_list(num1, op)

    num2, num_str2 = random_number2(num2_list)
    draw.text((40 * 2 + 15, (height - op_num2_size)/2), num_str2, font=font3, fill=color)

    results = calculate(num1, num2, op)

    # 模糊:
    # image = image.filter(ImageFilter.BLUR)

    # 生成验证码图片
    img_io = StringIO()
    image.save(img_io, 'jpeg')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.read())

    return results, img_base64


# res, img_base64 = generate_verify_code()
# <img src="data:image/jpg;base64,{{ img_io }}">
