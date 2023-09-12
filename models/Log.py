from base import db
from datetime import datetime


class Log(db.Model):
    __tablename__ = "logs"

    time = db.Column(db.DateTime(), default=datetime.now())
    u_id = db.Column(db.BigInteger)
    action = db.Column(db.SmallInteger)
    result = db.Column(db.String, nullable=True)
