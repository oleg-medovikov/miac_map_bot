from base import db


class Meddoc(db.Model):
    __tablename__ = "meddoc"
    id = db.Column(db.Integer, primary_key=True)
    # идентификатор в системе Региза
    meddoc_biz_key = db.Column(db.BigInteger)
    # идентификатор организации
    org_id = db.Column(db.SmallInteger, db.ForeignKey("org.id"))
    # идентификатор пациента
    p_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    # номер истории болезни
    history_number = db.Column(db.String(50))

    # различные даты
    creation_date = db.Column(db.Date)
    success_date = db.Column(db.Date)
    # численный идентификатор сэмда
    doc_type_code = db.Column(db.SmallInteger)

    # обработка документа reading
    r_id = db.Column(db.Integer, db.ForeignKey("reading.id"), nullable=True)
    # результат прочтения - случай case
    c_id = db.Column(db.Integer, db.ForeignKey("cases.id"), nullable=True)
    # наполнение контентом - что нашлось в сэмде
    cc_id = db.Column(db.Integer, db.ForeignKey("case_content.id"), nullable=True)

    @property
    def org(self):
        return self._org

    @org.setter
    def org(self, value):
        self._org = value

    @property
    def patient(self):
        return self._patient

    @patient.setter
    def patient(self, value):
        self._patient = value

    @property
    def reading(self):
        return self._reading

    @reading.setter
    def reading(self, value):
        self._reading = value

    @property
    def case(self):
        return self._cases

    @case.setter
    def case(self, value):
        self._cases = value

    @property
    def content(self):
        return self._case_content

    @content.setter
    def content(self, value):
        self._case_content = value
