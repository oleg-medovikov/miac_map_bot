from base import db


class MeddocCategory(db.Model):
    __tablename__ = "meddoc_category"

    id = db.Column(db.Integer, primary_key=True)
    m_id = db.Column(db.Integer, db.ForeignKey("meddoc.id"))
    c_id = db.Column(db.SmallInteger, db.ForeignKey("category.id"))

    @property
    def meddoc(self):
        return self._meddoc

    @meddoc.setter
    def meddoc(self, value):
        self._meddoc = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value
