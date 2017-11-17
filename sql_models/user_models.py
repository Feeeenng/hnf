# -*- coding: utf8 -*-
from __future__ import unicode_literals
from sql_models import BaseModelObject, db


class User(BaseModelObject):
    __tablename__ = 'user'
    # __table_args__ = {'autoload': True, 'extend_existing': True}

    name = db.Column(db.String(length=20), nullable=False)
    age = db.Column(db.Integer)

    def __unicode__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, self.id)