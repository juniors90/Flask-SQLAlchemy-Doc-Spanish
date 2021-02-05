SQLALCHEMY_DATABASE_URI = 'postgres://localhost/main'
SQLALCHEMY_BINDS = {
    'users': 'mysqldb://localhost/users',
    'appmeta': 'sqlite:////path/to/appmeta.db'
}

>>> db.create_all()
>>> db.create_all(bind=['users'])
>>> db.create_all(bind='appmeta')
>>> db.drop_all(bind=None)

class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

user_favorites = db.Table('user_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('message_id', db.Integer, db.ForeignKey('message.id')),
    info={'bind_key': 'users'}
)

from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr, has_inherited_table

class IdModel(Model):
    @declared_attr
    def id(cls):
        for base in cls.__mro__[1:-1]:
            if getattr(base, '__table__', None) is not None:
                type = sa.ForeignKey(base.id)
                break
        else:
            type = sa.Integer

        return sa.Column(type, primary_key=True)

db = SQLAlchemy(model_class=IdModel)

class User(db.Model):
    name = db.Column(db.String)

class Employee(User):
    title = db.Column(db.String)

from datetime import datetime

class TimestampMixin(object):
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

class Author(db.Model):
    ...

class Post(TimestampMixin, db.Model):
   ...

from flask_sqlalchemy import BaseQuery, SQLAlchemy

class GetOrQuery(BaseQuery):
    def get_or(self, ident, default=None):
        return self.get(ident) or default

db = SQLAlchemy(query_class=GetOrQuery)

# get a user by id, or return an anonymous user instance
user = User.query.get_or(user_id, anonymous_user)

class MyModel(db.Model):
    cousin = db.relationship('OtherModel', query_class=GetOrQuery)

class MyModel(db.Model):
    query_class = GetOrQuery

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import DefaultMeta, Model

class CustomMeta(DefaultMeta):
    def __init__(cls, name, bases, d):
        # custom class setup could go here

        # be sure to call super
        super(CustomMeta, cls).__init__(name, bases, d)

    # custom class-only methods could go here

db = SQLAlchemy(model_class=declarative_base(
    cls=Model, metaclass=CustomMeta, name='Model'))

from flask_sqlalchemy.model import BindMetaMixin, Model
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

class NoNameMeta(BindMetaMixin, DeclarativeMeta):
    pass

db = SQLAlchemy(model_class=declarative_base(
    cls=Model, metaclass=NoNameMeta, name='Model'))

