from base import db


class Case(db.Model):
    __tablename__ = "cases"

    id = db.Column(db.Integer, primary_key=True)
    # идентификатор врача
    d_id = db.Column(db.SmallInteger, db.ForeignKey("doctor.id"))
    # идентификатор адреса
    a_id = db.Column(db.Integer, db.ForeignKey("adress.id"))
    # идентификатор работы
    w_id = db.Column(db.Integer, db.ForeignKey("work.id"), nullable=True)
    # идентификатор диагноза
    di_id = db.Column(db.Integer, db.ForeignKey("diagnoz.id"))

    # дата заболевания
    date_sicness = db.Column(db.Date, nullable=True)
    # дата первого обращения
    date_first_req = db.Column(db.Date, nullable=True)
    # дата отправки заявки в СЕС
    time_SES = db.Column(db.DateTime, nullable=True)
    # дата установки диагноза
    date_diagnoz = db.Column(db.Date, nullable=True)

    # тип госпитализации
    hospitalization = db.Column(db.SmallInteger, nullable=True)
    # проведенные анти-эпидемиологические меры
    anti_epidemic_measures = db.Column(db.String, nullable=True)
    # лабораторное потверждение
    lab_confirm = db.Column(db.Boolean)

    @property
    def doctor(self):
        return self._doctor

    @doctor.setter
    def doctor(self, value):
        self._doctor = value

    @property
    def adress(self):
        return self._adress

    @adress.setter
    def adress(self, value):
        self._adress = value

    @property
    def work(self):
        return self._work

    @work.setter
    def work(self, value):
        self._work = value

    @property
    def diagnoz(self):
        return self._diagnoz

    @diagnoz.setter
    def diagnoz(self, value):
        self._diagnoz = value
