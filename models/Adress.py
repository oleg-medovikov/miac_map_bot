from base import db

from sqlalchemy.dialects.postgresql import UUID


class Adress(db.Model):
    __tablename__ = "adress"

    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.String)
    point = db.Column(db.ARRAY(db.Float))
    text = db.Column(db.String)
    fias = db.Column(UUID, nullable=True)
    street = db.Column(db.String(100), nullable=True)
    house = db.Column(db.String(20), nullable=True)
