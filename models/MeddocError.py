from base import db


class MeddocError(db.Model):
    __tablename__ = "meddoc_error"

    id = db.Column(db.Integer, primary_key=True)
    m_id = db.Column(db.Integer, db.ForeignKey("meddoc.id"))
    e_id = db.Column(db.SmallInteger, db.ForeignKey("errors.id"))

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
