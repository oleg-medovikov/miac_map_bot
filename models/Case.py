from base import db

from datetime import datetime


class Case(db.Model):
    __tablename__ = "cases"

    meddoc_biz_key = db.Column(db.BigInteger, primary_key=True)
    d_id = db.Column(db.SmallInteger)
    a_id = db.Column(db.Integer)
    date_sicness = db.Column(db.Date, nullable=True)
    date_first_req = db.Column(db.Date, nullable=True)
    hospitalization_type = db.Column(db.SmallInteger, nullable=True)
    primary_anti_epidemic_measures = db.Column(db.String, nullable=True)
    time_SES = db.Column(db.DateTime, nullable=True)
    w_id = db.Column(db.Integer)
    date_diagnoz = db.Column(db.Date, nullable=True)
    di_id = db.Column(db.Integer)
    lab_confirm = db.Column(db.Boolean)
    date_update = db.Column(db.DateTime(), default=datetime.now())
