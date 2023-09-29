from models import MeddocError


async def add_error(d_id: int, e_id: int):
    await MeddocError.delete.where(MeddocError.m_id == d_id).gino.status()

    await MeddocError.create(m_id=d_id, e_id=e_id)
