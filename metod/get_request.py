import aiohttp

from exept import NetricaError
from conf import settings


async def get_request(doc):
    URL = (
        settings.REGIZ_URL_2
        + str(doc.meddoc_biz_key)
        + "?mimeTypeOriginal=true&_format=json&IsIgnoreFHIRcode=true"
    )
    HEADER = dict(Authorization=settings.REGIZ_AUTH)

    async with aiohttp.ClientSession() as session:
        async with session.get(URL, headers=HEADER) as response:
            if response.status != 200:
                raise NetricaError("проблема с подключением\n" + URL)

            return await response.json()
