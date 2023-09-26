from base import db


class Reading(db.Model):
    __tablename__ = "reading"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    result = db.Column(db.Boolean)
