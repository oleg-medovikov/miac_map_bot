from base import db
from datetime import datetime


class Token(db.Model):
    __tablename__ = "tokens"

    token = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(20))
    count = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    date_update = db.Column(db.DateTime(), default=datetime.now())
