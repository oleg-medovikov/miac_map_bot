from base import db
from datetime import datetime


class Adress(db.Model):
    __tablename__ = "adresses"

    a_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    line = db.Column(db.String)
    fias = db.Column(db.String, nullable=True)
    point = db.Column(db.ARRAY(db.Float))
    text = db.Column(db.String)
    street = db.Column(db.String(100))
    house = db.Column(db.String(20))
    date_update = db.Column(db.DateTime(), default=datetime.now())
