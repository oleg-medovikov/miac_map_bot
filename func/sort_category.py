from sqlalchemy import or_, null

from models import Category, Meddoc, Patient, Case, Diagnoz
from metod import add_meddoc_category


async def sort_category() -> None:
    """прогоняем меддоки на соответсвие категориям заболеваний"""

    for category in await Category.query.guno.all():
        # первым делом вытаскиваем id всех подходящих диагнозов для категории
        query = (
            await Diagnoz.select("id")
            .where(or_(Diagnoz.mkb.in_(category.mkb), Diagnoz.mkb3.in_(category.mkb3)))
            .gino.all()
        )
        # превращаем список кортежей в список id
        DIAGNOZIS = [_[0] for _ in query]
        # выбираем те меддокументы, где есть случаи с нужными диагнозами
        query = Meddoc.load(patient=Patient, case=Case).where(Case.di_id.in_(DIAGNOZIS))
        # проверка на пол
        if "sex" in category.demind:
            query = query.where(Patient.sex == category.demind["sex"])
        # проверка на максимальный возраст
        if "age_end" in category.demaind:
            query = query.where(Meddoc.age < category.demaind["age_end"])
        # проверка на минимальный возраст
        if "age_start" in category.demaind:
            query = query.where(Meddoc.age >= category.demaind["age_start"])
        # проверка на рождение ребенка в ближайшие 45 дней
        if "birthdate_baby" in category.demaind:
            query = query.where(Patient.birthdate_baby != null())
        # добавляем категорию меддокам
        for document in await query.gino.all():
            await add_meddoc_category(m_id=document.id, c_id=category.id)
