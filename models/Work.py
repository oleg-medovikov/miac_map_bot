from base import db
from datetime import datetime

"""
все что связано с адресом работы перенес в таблицу адресов,
оставил тут только a_id
"""


class Work(db.Model):
    __tablename__ = "works"

    w_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True)
    a_id = db.Column(db.Integer)
    date_update = db.Column(db.DateTime(), default=datetime.now())
