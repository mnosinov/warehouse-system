from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None