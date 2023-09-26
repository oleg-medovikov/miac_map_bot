from base import db

"""
все что связано с адресом работы перенес в таблицу адресов,
оставил тут только a_id
"""


class Work(db.Model):
    __tablename__ = "work"

    id = db.Column(db.Integer, primary_key=True)
    a_id = db.Column(db.Integer, db.ForeignKey("adress.id"))
    name = db.Column(db.String, nullable=True)

    @property
    def adress(self):
        return self._adress

    @adress.setter
    def adress(self, value):
        self._adress = value
