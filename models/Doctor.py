from base import db
from datetime import datetime


class Doctor(db.Model):
    __tablename__ = "doctors"

    d_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    org = db.Column(db.String)
    fio = db.Column(db.String(200))
    telefon = db.Column(db.String(20))
    spec = db.Column(db.String)
    date_update = db.Column(db.DateTime(), default=datetime.now())
