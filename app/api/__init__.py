from fastapi import APIRouter

from api.health import router as health_router
from api.prediction import router as predicion_router


router = APIRouter()


router.include_router(health_router)
router.include_router(predicion_router)
