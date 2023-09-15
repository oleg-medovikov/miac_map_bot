from base import db
from datetime import datetime


class Work(db.Model):
    __tablename__ = "works"

    w_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    line = db.Column(db.String)
    name = db.Column(db.String, nullable=True)
    fias = db.Column(db.String, nullable=True)
    point = db.Column(db.ARRAY(db.Float))
    text = db.Column(db.String)
    date_update = db.Column(db.DateTime(), default=datetime.now())
