from pydantic import BaseModel


class PhishingPredictionResult(BaseModel):
    prediction: int
