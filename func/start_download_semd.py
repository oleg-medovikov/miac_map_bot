from aiogram import md
from sqlalchemy import and_, false, true
from datetime import datetime


from models import Reading
from metod import add_error, delete_error
from exept import (
    NoTokenYandex,
    NetricaError,
    NoCDAfiles,
    CDAisEmpty,
    NoFindReg,
    NoFindMKB,
    NoCorrectMKB,
    TokenYandexExceed,
)
from .parsing_semd import parsing_semd
from conf import settings
from disp import bot


async def start_download_semd(DOCS: list):
    STAT = {
        "count": len(DOCS),
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
            print("ошибка яндекса")
            continue
        except NetricaError:
            STAT["skip"] += 1
            await doc.update(r_id=read_false.id).apply()
            print(doc.meddoc_biz_key, "ошибка нетрики")
            continue
        except NoCDAfiles:
            # нулевая ошибка обработки, нет файла
            await add_error(doc.id, 0)
            await doc.update(r_id=read_false.id).apply()
            STAT["error"] += 1
            print(doc.meddoc_biz_key, "нет файлов CDA")
            continue
        except NoFindReg:
            # Не найден адрес регистрации
            await add_error(doc.id, 1)
            await doc.update(r_id=read_false.id).apply()
            print(doc.meddoc_biz_key, "не найден адрес регистрации")
            STAT["error"] += 1
            continue
        except NoFindMKB:
            # не найден диагноз!
            await add_error(doc.id, 2)
            await doc.update(r_id=read_false.id).apply()
            print(doc.meddoc_biz_key, "не найден мкб")
            STAT["error"] += 1
            continue
        except NoCorrectMKB:
            # не найден диагноз!
            await add_error(doc.id, 4)
            await doc.update(r_id=read_false.id).apply()
            print(doc.meddoc_biz_key, "некорректный мкб")
            STAT["error"] += 1
            continue
        except CDAisEmpty:
            # просто пустой файл
            await add_error(doc.id, 3)
            await doc.update(r_id=read_false.id).apply()
            STAT["error"] += 1
        else:
            await delete_error(doc.id)
            await doc.update(r_id=read_true.id, c_id=case.id).apply()
            STAT["done"] += 1

    mess = (
        f'Всего файлов для обработки: {STAT["count"]}'
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
