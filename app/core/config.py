from starlette.datastructures import CommaSeparatedStrings
from typing import List
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

APP_VERSION = "0.0.1"
API_PREFIX = "/api"
APP_NAME: str = config("APP_NAME", default="Client API")

HOST: str = config("HOST", default='0.0.0.0')
PORT: int = config("PORT", cast=int, default=8080)


API_KEY: Secret = config("API_KEY", cast=Secret)
IS_DEBUG: bool = config("IS_DEBUG", cast=bool, default=False)

DEFAULT_MODEL_PATH: str = config("DEFAULT_MODEL_PATH")

ALLOWED_HOSTS: List[str] = list(
    config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="*"))
