# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from es_models import *

my_pinyin = token_filter('my_pinyin', type='pinyin', first_letter='prefix', padding_char='')

ik_smart_pinyin_analyzer = analyzer('ik_smart_pinyin_analyzer', tokenizer='ik_smart',
                                    filter=[my_pinyin, 'word_delimiter'])

ik_max_word_pinyin_analyzer = analyzer('ik_max_word_pinyin_analyzer', tokenizer='ik_max_word',
                                       filter=[my_pinyin, 'word_delimiter'])


class Comment(InnerObjectWrapper):
    def func(self):
        return '[{0}]:{1}'.format(self.author, self.content)


class User(DocType):
    name = Keyword(fields={
        'pinyin': Text(analyzer=ik_max_word_pinyin_analyzer, search_analyzer=ik_smart_pinyin_analyzer)
    })
    age = Integer()
    desc = Text(analyzer='ik_smart')
    hobbies = Keyword()  # 列表
    created_at = Date()  # datetime类型
    is_ready = Boolean()  # bool
    comments = Nested(  # 内嵌对象
        doc_class=Comment,
        include_in_parent=True,
        properties={
            'author': Text(analyzer=ik_max_word_pinyin_analyzer, search_analyzer=ik_smart_pinyin_analyzer),
            'content': Text(analyzer='ik_smart'),
            'created_at': Date()
        }
    )

    class Meta:
        index = 'hnf'  # 索引(数据库)
        doc_type = 'users'  # 类型(表)

    def add_comment(self, author, content):
        self.comments.append({
            'author': author,
            'content': content
        })
        return self

    @classmethod
    def get_mapping(cls):
        return cls._doc_type.mapping.to_dict()

    def save(self, *args, **kwargs):
        # pre_save 保存前处理
        self.created_at = datetime.datetime.now()
        return super(User, self).save(*args, **kwargs)