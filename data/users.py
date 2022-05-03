import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin


class Users(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    lesson = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    day = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=True)
