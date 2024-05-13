from fastapi import APIRouter, Depends
from starlette.requests import Request

from core import security
from models.payload import PhishingPayload
from models.prediction import PhishingPredictionResult
from services.model_service import PhishingModel

router = APIRouter()


@router.post("/predict", response_model=PhishingPredictionResult, name="predict")
def post_predict(
    request: Request,
    block_data: PhishingPayload,
    _: bool = Depends(security.validate_request),
) -> PhishingPredictionResult:
    model: PhishingModel = request.app.state.model
    prediction: PhishingPredictionResult = model.predict(block_data)

    return prediction
