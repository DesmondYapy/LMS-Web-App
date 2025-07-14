# models/response.py

from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime


class LoginResponse(BaseModel):
    token: str
    role: str


class InstructorCoursesResponse(BaseModel):
    instructor_courses: List[str]


class OverviewStatsResponse(BaseModel):
    total_topics: int
    total_students: int
    total_entries: int
    topic_counts: Dict[str, int]


class AtRiskStudent(BaseModel):
    user_id: int
    user_name: str
    course_code: str
    num_entries: int


class AtRiskResponse(BaseModel):
    at_risk_students: List[AtRiskStudent]
    at_risk_total: Dict[str, int]


class CourseStatsResponse(BaseModel):
    course_name: str
    total_topics: int
    total_students: int
    total_entries: int
    entries_per_topic: Dict[str, int]
    weekly_topic_counts: Dict[str, Dict[str, int]]


class StudentStats(BaseModel):
    user_id: int
    user_name: str
    semester: str
    num_entries: int
    num_topics: int


class TopStudentsResponse(BaseModel):
    top_3_students: List[StudentStats]
    list_of_students: List[StudentStats]


class Entry(BaseModel):
    entry_content: Optional[str]
    entry_created_at: Optional[datetime]
    user_name: Optional[str]


class Topic(BaseModel):
    topic_id: int
    topic_title: str
    topic_content: str
    entries: List[Entry]


class DiscussionBoardResponse(BaseModel):
    topics: List[Topic]


class StudentResponse(BaseModel):
    user_id: int
    total_topics: int
    total_entries: int
    filtered_merged_df: List[Dict[str, str]]  # list of dict rows from DataFrame
