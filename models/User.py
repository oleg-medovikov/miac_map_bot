from base import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.SmallInteger, primary_key=True)
    chat_id = db.Column(db.BigInteger)
    fio = db.Column(db.String(length=200))
    role = db.Column(db.String(length=20))
    date_update = db.Column(db.DateTime(), default=datetime.now())
