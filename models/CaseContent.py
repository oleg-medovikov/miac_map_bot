from base import db


class CaseContent(db.Model):
    __tablename__ = "case_content"

    id = db.Column(db.Integer, primary_key=True)
    doc_fio = db.Column(db.Boolean)
    doc_telefon = db.Column(db.Boolean)
    doc_spec = db.Column(db.Boolean)
    doc_snils = db.Column(db.Boolean)
    adress_reg = db.Column(db.Boolean)
    adress_reg_fias = db.Column(db.Boolean)
    date_sickness = db.Column(db.Boolean)
    date_first_req = db.Column(db.Boolean)
    hospitalization = db.Column(db.Boolean)
    measures = db.Column(db.Boolean)
    time_SES = db.Column(db.Boolean)
    work_adress = db.Column(db.Boolean)
    work_adress_fias = db.Column(db.Boolean)
    work_name = db.Column(db.Boolean)
    work_last_date = db.Column(db.Boolean)
    date_diagnoz = db.Column(db.Boolean)
    diagnoz = db.Column(db.Boolean)
    MKB = db.Column(db.Boolean)
    lab_confirm = db.Column(db.Boolean)
