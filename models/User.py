from base import db
from sqlalchemy import func


class User(db.Model):
    __tablename__ = 'users'

    u_id = db.Column(db.BigInteger, primary_key=True)
    fio  = db.Column(db.String(length=200))
    role = db.Column(db.String(length=20))
    date_update = db.Column(db.DateTime(timezone=True), default=func.now())
