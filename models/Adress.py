from base import db
from datetime import datetime


class Adress(db.Model):
    __tablename__ = "adresses"

    line = db.Column(db.String, primary_key=True)
    point = db.Column(db.ARRAY(db.Float))
    text = db.Column(db.String)
    street = db.Column(db.String(leght=100))
    house = db.Column(db.String(leght=20))
    date_update = db.Column(db.DateTime(), default=datetime.now())
