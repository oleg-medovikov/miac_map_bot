from base import db
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID


class Work(db.Model):
    __tablename__ = "works"

    w_id = db.Column(db.Integer, primory_key=True)
    line = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=True)
    fias = db.Column(UUID, nullable=True)
    point = db.Column(db.ARRAY(db.Float))
    text = db.Column(db.String)
    date_update = db.Column(db.DateTime(), default=datetime.now())
