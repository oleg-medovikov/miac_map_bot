from asyncpg.exceptions import UniqueViolationError
from aiogram import md
from sqlalchemy import and_, false, true
from datetime import datetime

from models import MeddocError, Reading
from exept import (
    NoTokenYandex,
    NetricaError,
    NoCDAfiles,
    NoFindReg,
    NoFindMKB,
    TokenYandexExceed,
)
from .parsing_semd import parsing_semd
from conf import settings
from disp import bot


async def start_download_semd(DOCS: list):
    STAT = {
        "count": len(DOCS),
        "double": 0,
        "skip": 0,
        "error": 0,
        "done": 0,
    }
    read_false = await Reading.query.where(
        and_(
            Reading.date == datetime.today(),
            Reading.result == false(),
        )
    ).gino.first()
    if read_false is None:
        read_false = await Reading.create(date=datetime.today(), result=False)
    read_true = await Reading.query.where(
        and_(
            Reading.date == datetime.today(),
            Reading.result == true(),
        )
    ).gino.first()
    if read_true is None:
        read_true = await Reading.create(date=datetime.today(), result=True)

    for doc in DOCS:
        try:
            case = await parsing_semd(doc)
        except UniqueViolationError:
            STAT["double"] += 1
            continue
        except NoTokenYandex:
            await bot.send_message(
                settings.MASTER,
                "Закончились Токены и я закончил",
                disable_notification=True,
                parse_mode="MarkdownV2",
            )
            break
        except TokenYandexExceed:
            # что-то случилось с геокодером, просто идем далее
            STAT["skip"] += 1
            await doc.update(r_id=read_false.id).apply()
            continue
        except NetricaError:
            STAT["skip"] += 1
            await doc.update(r_id=read_false.id).apply()
            continue
        except NoCDAfiles:
            # нулевая ошибка обработки, нет файла
            await MeddocError.create(meddoc=doc.id, error=0)
            await doc.update(r_id=read_false.id).apply()
            STAT["error"] += 1
            continue
        except NoFindReg:
            # Не найден адрес регистрации
            await MeddocError.create(meddoc=doc.id, error=1)
            await doc.update(r_id=read_false.id).apply()
            STAT["error"] += 1
            continue
        except NoFindMKB:
            # не найден диагноз!
            await MeddocError.create(meddoc=doc.id, error=2)
            await doc.update(r_id=read_false.id).apply()
            STAT["error"] += 1
            continue

        except Exception as e:
            await doc.update(error=True).apply()
            STAT["error"] += 1
            await bot.send_message(
                settings.MASTER,
                md.quote(str(e) + f"\n {doc.meddoc_biz_key}"),
                disable_notification=True,
                parse_mode="MarkdownV2",
            )
        else:
            await doc.update(r_id=read_true.id, c_id=case.id).apply()
            STAT["done"] += 1

    mess = (
        f'Всего файлов для обработки: {STAT["count"]}'
        + f'\nПовторно обработаны: {STAT["double"]}'
        + f'\nПропущено: {STAT["skip"]}'
        + f'\nОшибки: {STAT["error"]}'
        + f'\nОбработано успешно: {STAT["done"]}'
    )

    await bot.send_message(
        settings.MASTER,
        md.quote(mess),
        disable_notification=True,
        parse_mode="MarkdownV2",
    )
