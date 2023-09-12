from base import db
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID


class Org(db.Model):
    __tablename__ = "orgs"

    org_id = db.Column(db.SmallInteger, primary_key=True)
    case_level1_key = db.Column(UUID)
    short_name = db.Column(db.String)
    date_update = db.Column(db.DateTime(), default=datetime.now())
