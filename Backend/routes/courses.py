import pandas as pd

from fastapi import APIRouter

from models.request import InstructorCoursesRequest, CourseStatsRequest
from models.response import InstructorCoursesResponse, CourseStatsResponse

from utils.data_loader import topics, entries, courses, enrollments

router = APIRouter()


@router.post("/instructor-courses", response_model=InstructorCoursesResponse)
def get_instructor_courses(data: InstructorCoursesRequest) -> InstructorCoursesResponse:
    """
    Returns the list of courses an instructor teaches
    Admins will see all courses.
    """

    # TODO: Replace with real database query
    all_courses = ["TEK102", "SRF305", "IHU224", "LOH116", "YDF451"]
    instructor_courses = ["TEK102", "IHU224", "LOH116"]

    # TODO: Extract role based on JWT passed in via middleware
    if data.role == "admin":
        return InstructorCoursesResponse(instructor_courses=all_courses)
    else:
        return InstructorCoursesResponse(instructor_courses=instructor_courses)


@router.post("/course-stats", response_model=CourseStatsResponse)
def get_course_specific_stats(data: CourseStatsRequest) -> CourseStatsResponse:
    """
    Returns the course specific statistics
    """

    course_code = data.course_code
    course_name = courses[courses["course_code"] == course_code]["course_name"].iloc[0]

    # Merge DataFrames
    merged_t_ent_c = topics.merge(entries, on="topic_id", how="left").merge(
        courses, on="course_id", how="left"
    )

    merged_e_c = enrollments.merge(courses, on="course_id")

    # Filter DataFrame
    filtered_merged_t_ent_c = merged_t_ent_c[
        merged_t_ent_c["course_code"] == course_code
    ]
    filtered_merged_e_c = merged_e_c[
        (merged_e_c["course_code"] == course_code)
        & (merged_e_c["enrollment_state"] == "active")
    ]

    # Extract Stats
    total_topics = filtered_merged_t_ent_c["topic_title"].nunique()
    total_students = filtered_merged_e_c["user_id"].nunique()
    total_entries = filtered_merged_t_ent_c["entry_id"].nunique()

    # Extract line chart data of weekly entries by topic
    filtered_merged_t_ent_c["entry_created_at"] = pd.to_datetime(
        filtered_merged_t_ent_c["entry_created_at"]
    )
    filtered_merged_t_ent_c = filtered_merged_t_ent_c.dropna(
        subset=["entry_created_at"]
    )
    filtered_merged_t_ent_c["week"] = (
        filtered_merged_t_ent_c["entry_created_at"]
        .dt.to_period("W")
        .apply(lambda r: r.start_time)
    )
    weekly_topic_counts = (
        filtered_merged_t_ent_c.groupby(["week", "topic_title"])
        .size()
        .reset_index(name="num_entries")
    )
    pivot_df = weekly_topic_counts.pivot(
        index="week", columns="topic_title", values="num_entries"
    ).fillna(0)
    pivot_df = pivot_df.sort_index()
    pivot_df.index = pivot_df.index.astype(str)
    weekly_topic_counts = pivot_df.astype(int).to_dict(orient="index")

    entries_per_topic = (
        filtered_merged_t_ent_c["topic_title"].value_counts().sort_index()
    )

    return CourseStatsResponse(
        course_name=course_name,
        total_topics=total_topics,
        total_students=total_students,
        total_entries=total_entries,
        entries_per_topic=entries_per_topic.to_dict(),
        weekly_topic_counts=weekly_topic_counts,
    )
