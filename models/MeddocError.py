from base import db


class MeddocError(db.Model):
    __tablename__ = "meddoc_error"

    id = db.Column(db.Integer, primary_key=True)
    meddoc = db.Column(db.Integer, db.ForeignKey("meddoc.id"))
    error = db.Column(db.SmallInteger, db.ForeignKey("error.id"))

    @property
    def meddoc(self):
        return self._meddoc

    @meddoc.setter
    def meddoc(self, value):
        self._meddoc = value

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value
