import datetime
import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from flask_login import UserMixin


class Names(SqlAlchemyBase, UserMixin):
    __tablename__ = 'teachers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subject = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("subjects.id"),
                                index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = orm.relation("Subjects")
