from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# from pydantic.types import conint

class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    fullname: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    fullname: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
