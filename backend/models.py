from pydantic import BaseModel

class RatingRequest(BaseModel):
    proID: str
    songID: str
    rate: float

class LoginRequest(BaseModel):
    nick: str
    password: str

class SignupRequest(BaseModel):
    nick: str
    password: str