from base import db


class Meddoc(db.Model):
    __tablename__ = "meddocs"

    meddoc_biz_key = db.Column(db.BigInteger, primary_key=True)
    creation_date = db.Column(db.Date)
    success_date = db.Column(db.Date)
    birthdate = db.Column(db.Date, nullable=True)
    org_id = db.Column(db.SmallInteger)
    history_number = db.Column(db.String(50))
    doc_type_code = db.Column(db.SmallInteger)
    processed = db.Column(db.Boolean, default=False)
    error = db.Column(db.Boolean, default=False)
