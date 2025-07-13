# models/response.py

from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

class LoginResponse(BaseModel):
    token: str
    role: str


class InstructorCoursesResponse(BaseModel):
    instructor_courses : List[str]


class OverviewStatsResponse(BaseModel):
    total_topics : int
    total_students : int
    total_entries : int
    topic_counts : Dict[str, int]
