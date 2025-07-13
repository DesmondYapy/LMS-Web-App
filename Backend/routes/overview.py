from fastapi import APIRouter, Depends, HTTPException

from models.request import OverviewStatsRequest
from models.response import OverviewStatsResponse

from utils.data_loader import topics, entries, courses, enrollments

router = APIRouter()

@router.post("/overview-stats", response_model=OverviewStatsResponse)
def get_overview_stats(data: OverviewStatsRequest) -> OverviewStatsResponse:


    """
    Returns overview stats for all instructor courses
    """

    instructor_courses = data.instructor_courses

    # Merge dataframes
    merged_t_ent_c = topics \
        .merge(entries, on="topic_id", how="left") \
        .merge(courses, on="course_id", how="left")
    merged_e_c = enrollments.merge(courses, on="course_id")
    merged_t_c = topics.merge(courses, on="course_id")

    # Filter dataframes based on instructor courses
    filtered_merged_t_ent_c = merged_t_ent_c[
    merged_t_ent_c['course_code'].isin(instructor_courses)
    ]
    filtered_merged_e_c = merged_e_c[
        (merged_e_c['course_code'].isin(instructor_courses)) &
        (merged_e_c['enrollment_state'] == 'active')
    ]
    filtered_merged_t_c = merged_t_c[
        merged_t_c['course_code'].isin(instructor_courses)
    ]
    
    # Extract stats
    total_topics = filtered_merged_t_ent_c['topic_title'].nunique()
    total_students = filtered_merged_e_c['user_id'].nunique()
    total_entries = filtered_merged_t_ent_c['entry_id'].nunique()
    topic_counts = filtered_merged_t_c['course_code'].value_counts().sort_index()


    return OverviewStatsResponse(
        total_topics=total_topics,
        total_students=total_students,
        total_entries=total_entries,
        topic_counts=topic_counts.to_dict()
    )

