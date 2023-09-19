from base import db


class Error(db.Model):
    __tablename__ = "errors"

    e_id = db.Column(db.Integer, primary_key=True)
    meddoc_biz_key = db.Column(db.BigInteger)
    error = db.Column(db.SmallInteger)
