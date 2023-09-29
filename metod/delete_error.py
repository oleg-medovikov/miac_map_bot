from models import MeddocError


async def delete_error(d_id: int):
    await MeddocError.delete.where(MeddocError.m_id == d_id).gino.status()
