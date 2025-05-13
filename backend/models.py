from pydantic import BaseModel

class RatingRequest(BaseModel):
    proID: str
    songID: str
    rate: float