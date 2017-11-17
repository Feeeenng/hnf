# -*- coding: utf8 -*-
from datetime import datetime

from app import sql_db as db
from utils.datetime_utils import format_datetime, now_lambda, timedelta


def create_tables():
    db.create_all()


def drop_tabels():
    db.drop_all()


class BaseModelObject(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True))
    updated_at = db.Column(db.DateTime(timezone=True))
    deleted_at = db.Column(db.DateTime(timezone=True))

    def __init__(self, *args, **kwargs):
        super(BaseModelObject, self).__init__(*args, **kwargs)

    def save(self):
        now = datetime.utcnow()
        if not self.id:
            self.created_at = now

        self.updated_at = now
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as ex:
            db.session.rollback()

    @classmethod
    def from_id(cls, id):
        obj = cls.query.filter_by(id=id).first()
        return obj

    @classmethod
    def from_db(cls, **kwargs):
        if len(kwargs.items()) <= 0:
            return None

        expressions = cls.get_filter_params(**kwargs)
        obj = cls.query.filter(*expressions).first()
        return obj

    @classmethod
    def fetch(cls, page=0, count=0, sort_key=None, **kwargs):
        sort_field = cls.get_sort_field(sort_key)
        if page == 0 and count == 0:
            expressions = cls.get_filter_params(**kwargs)
            objs = cls.query.filter(*expressions).order_by(sort_field).all()
        else:
            expressions = cls.get_filter_params(**kwargs)
            objs = cls.query.filter(*expressions).order_by(sort_field).paginate(page, count, False).items
        return objs

    @classmethod
    def total_counts(cls, **kwargs):
        expressions = cls.get_filter_params(**kwargs)
        count = cls.query.filter(*expressions).count()
        return count

    @classmethod
    def get_filter_params(cls, **kwargs):
        expressions = []
        for k, v in kwargs.items():
            if '__' in k:
                key = k.split('__')[0]
                operate = k.split('__')[1]
                if hasattr(cls, key):
                    field = getattr(cls, key)
                    if operate == 'contains':
                        expressions.append(field.contains(v))
                    elif operate == 'gt':
                        expressions.append(field > v)
                    elif operate == 'gte':
                        expressions.append(field >= v)
                    elif operate == 'lt':
                        expressions.append(field < v)
                    elif operate == 'lte':
                        expressions.append(field <= v)
                    elif operate == 'not':
                        expressions.append(field != v)
                    elif operate == 'in':
                        expressions.append(field.in_(v))
                    elif operate == 'not_in':
                        expressions.append(field.notin_(v))
                    elif operate == 'binary':
                        expressions.append(field.collate('utf8mb4_bin') == v)
                    elif operate == 'binary__contains':
                        expressions.append(field.collate('utf8mb4_bin').contains(v))
                    else:
                        raise SyntaxError, '无操作符{0}'.format(operate)
                else:
                    raise SyntaxError, 'models {0}无{1}字段'.format(cls.__name__, key)
            else:
                if hasattr(cls, k):
                    field = getattr(cls, k)
                    expressions.append(field == v)
                else:
                    raise SyntaxError, 'models {0}无{1}字段'.format(cls.__name__, k)

        return expressions

    @classmethod
    def get_sort_field(cls, field=None):
        if not field:
            return db.desc('id')

        if field.startswith('-'):
            field = field.strip('-')
            return db.desc(field)
        else:
            return db.asc(field)

    def object_as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_dict(self):
        d = self.object_as_dict()
        for k, v in d.items():
            if isinstance(v, datetime):
                v += timedelta(hours=8)
                v = v.strftime('%Y-%m-%d %H:%M:%S')
                d[k] = v
        return d