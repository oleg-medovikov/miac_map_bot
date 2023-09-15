from base import db
from datetime import datetime


class Diagnoz(db.Model):
    __tablename__ = "diagnozis"

    di_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MKB = db.Column(db.String(10))
    diagnoz = db.Column(db.String())
    date_update = db.Column(db.DateTime(), default=datetime.now())
