from starlette.config import Config

config = Config(".conf")

TELEGRAM_TOKEN = config("BOT_API", cast=str)
DATABASE_URL = config("DATABASE_URL", cast=str)

REGIZ_AUTH = config("REGIZ_AUTH", cast=str)
REGIZ_URL = config("REGIZ_URL", cast=str)
REGIZ_TOKEN = config("REGIZ_TOKEN", cast=str)

MASTER = config("MASTER", cast=int)
PROXY_URL = config("PROXY_URL", cast=str)
