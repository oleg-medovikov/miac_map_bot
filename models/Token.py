from base import db
from datetime import datetime


class Token(db.Model):
    __tablename__ = "tokens"

    token = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(leght=20))
    count = db.Column(db.Integer)
    date_update = db.Column(db.DateTime(), default=datetime.now())
