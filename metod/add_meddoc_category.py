from models import MeddocCategory
from sqlalchemy import and_


async def add_meddoc_category(m_id: int, c_id: int):
    medcat = await MeddocCategory.query.where(
        and_(MeddocCategory.m_id == m_id, MeddocCategory.c_id == c_id)
    ).gino.first()
    if medcat is None:
        await MeddocCategory.create(m_id=m_id, c_id=c_id)
