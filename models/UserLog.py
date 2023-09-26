from base import db
from datetime import datetime


class UserLog(db.Model):
    __tablename__ = "user_log"

    time = db.Column(db.DateTime(), default=datetime.now())
    # номер пользователя
    u_id = db.Column(db.SmallInteger, db.ForeignKey("user.id"))
    # номер действия
    a_id = db.Column(db.SmallInteger, db.ForeignKey("user_action.id"))

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def action(self):
        return self._user_action

    @action.setter
    def action(self, value):
        self._user_action = value
