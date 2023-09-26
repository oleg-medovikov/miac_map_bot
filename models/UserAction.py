from base import db


class UserAction(db.Model):
    __tablename__ = "user_action"

    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String)
