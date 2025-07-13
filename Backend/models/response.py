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


class AtRiskStudent(BaseModel):
    user_id: int
    user_name: str
    course_code: str
    num_entries: int


class AtRiskResponse(BaseModel):
    at_risk_students: List[AtRiskStudent]
    at_risk_total: Dict[str, int]


class CourseStatsResponse(BaseModel):
    total_topics: int
    total_students: int
    total_entries: int
    entries_per_topic: Dict[str, int]
    weekly_topic_counts: Dict[str, Dict[str, int]]

