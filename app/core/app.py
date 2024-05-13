from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from core.event_handlers import startup_handler, shutdown_handler, http_error_handler, http422_error_handler
from core.config import ALLOWED_HOSTS, API_PREFIX, IS_DEBUG, APP_NAME, APP_VERSION

from api import router as api_router
app = FastAPI(title=APP_NAME, debug=IS_DEBUG, version=APP_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_event_handler("startup", startup_handler(app))
app.add_event_handler("shutdown", shutdown_handler(app))
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)

app.include_router(api_router, prefix=API_PREFIX)
