from sqlalchemy.dialects.postgresql import UUID
from base import db


class Patient(db.Model):
    __tablename__ = "patient"

    id = db.Column(db.Integer, primary_key=True)
    # глобальный идентификатор
    global_id = db.Column(UUID)
    sex = db.Column(db.Boolean)
    # дата рождения
    birthdate = db.Column(db.Date)
    # дата рождения ребенка, если есть
    birthdate_baby = db.Column(db.Date, nullable=True)
