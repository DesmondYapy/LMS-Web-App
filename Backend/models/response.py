# models/response.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LoginResponse(BaseModel):
    token: str
    role: str

class EntryResponse(BaseModel):
    id: int
    topic_id: int
    content: str
    created_at: datetime

class UserSummary(BaseModel):
    id: int
    name: str
    post_count: int
    last_login: Optional[datetime]
