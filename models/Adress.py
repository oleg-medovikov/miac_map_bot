from base import db
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID


class Adress(db.Model):
    __tablename__ = "adresses"

    a_id = db.Column(db.Integer, primory_key=True)
    line = db.Column(db.String, primary_key=True)
    fias = db.Column(UUID, nullable=True)
    point = db.Column(db.ARRAY(db.Float))
    text = db.Column(db.String)
    street = db.Column(db.String(100))
    house = db.Column(db.String(20))
    date_update = db.Column(db.DateTime(), default=datetime.now())
