# models/request.py

from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class PostEntryRequest(BaseModel):
    topic_id: int
    content: str
