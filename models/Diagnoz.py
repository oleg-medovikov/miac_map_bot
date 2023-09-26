from base import db


class Diagnoz(db.Model):
    __tablename__ = "diagnoz"

    id = db.Column(db.Integer, primary_key=True)
    MKB = db.Column(db.String(10))
    diagnoz = db.Column(db.String())
