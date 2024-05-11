from pydantic import BaseModel


class PhishingPayload(BaseModel):
    url: str
