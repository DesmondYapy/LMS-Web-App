# models/request.py

from pydantic import BaseModel
from typing import List, Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class InstructorCoursesRequest(BaseModel):
    instructor_id: int
    role: Optional[str] = "Instructor"


class OverviewStatsRequest(BaseModel):
    instructor_courses: List[str]


class AtRiskRequest(BaseModel):
    instructor_courses: List[str]


class CourseStatsRequest(BaseModel):
    course_code: str


class TopStudentsRequest(BaseModel):
    course_code: str


class DiscussionBoardRequest(BaseModel):
    course_code: str
