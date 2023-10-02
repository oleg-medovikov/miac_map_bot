from base import db


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    color = db.Column(db.ARRAY(db.Float))
    mkb = db.Column(db.ARRAY(db.String))
    demaind = db.Column(db.JSON)
    active = db.Column(db.Boolean)
