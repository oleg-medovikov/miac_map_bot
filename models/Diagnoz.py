from base import db


class Diagnoz(db.Model):
    __tablename__ = "diagnoz"

    id = db.Column(db.Integer, primary_key=True)
    mkb = db.Column(db.String(10))
    mkb3 = db.Column(db.String(3))
    diagnoz = db.Column(db.String())
