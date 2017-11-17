# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from elasticsearch_dsl import DocType, Text, Keyword, Integer, Date, Q, Nested, InnerObjectWrapper, analyzer, \
    token_filter, Mapping, Boolean
from elasticsearch_dsl.connections import connections
from configs.config import conf

connections.create_connection(hosts=['{0}:{1}'.format(conf.ES_HOST, conf.ES_PORT)])  # 连接
