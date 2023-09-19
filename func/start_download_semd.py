from asyncpg.exceptions import UniqueViolationError
from aiogram import md


from models import Error
from exept import NoTokenYandex, NoCDAfiles, NoFindReg, NoFindMKB, TokenYandexExceed
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
    for doc in DOCS:
        error = await Error.query.where(
            Error.meddoc_biz_key == doc.meddoc_biz_key
        ).gino.first()
        if error is not None:
            STAT["skip"] += 1
            continue

        try:
            await parsing_semd(doc)
        except UniqueViolationError:
            await doc.update(processed=True).apply()
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
            continue
        except NoCDAfiles:
            # нулевая ошибка обработки, нет файла
            await Error.create(meddoc_biz_key=doc.meddoc_biz_key, error=0)
            STAT["error"] += 1
            continue
        except NoFindReg:
            # Не найден адрес регистрации
            await Error.create(meddoc_biz_key=doc.meddoc_biz_key, error=1)
            STAT["error"] += 1
            continue
        except NoFindMKB:
            # не найден диагноз!
            await Error.create(meddoc_biz_key=doc.meddoc_biz_key, error=2)
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
            await doc.update(processed=True).apply()
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
