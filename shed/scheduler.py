from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .get_meddocs import get_meddoc_automatic
from .refresh_tokens import refresh_tokens
from .download_semds import download_semds_automatic


def create_scheduler():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    scheduler.add_job(get_meddoc_automatic, trigger="cron", hour=5, minute=30)

    scheduler.add_job(refresh_tokens, trigger="cron", hour=7, minute=30)

    scheduler.add_job(download_semds_automatic, trigger="cron", hour=7, minute=31)

    return scheduler
