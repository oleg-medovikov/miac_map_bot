from base import db


class Error(db.Model):
    __tablename__ = "errors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
