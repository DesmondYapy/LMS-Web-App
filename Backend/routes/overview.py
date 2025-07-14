from fastapi import APIRouter

from models.request import OverviewStatsRequest, AtRiskRequest
from models.response import OverviewStatsResponse, AtRiskResponse

from utils.data_loader import topics, entries, courses, enrollments, users

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


@router.post("/at-risk", response_model=AtRiskResponse)
def get_at_risk_students(data: AtRiskRequest) -> AtRiskResponse:


    """
    Returns at risk students
    """

    instructor_courses = data.instructor_courses
    course_ids = courses[courses['course_code'].isin(instructor_courses)]['course_id'].tolist()

    # Merge DataFrames
    merged_e_c_u = enrollments \
        .merge(courses, on="course_id") \
        .merge(users, on='user_id')
    merged_ent_t = entries.merge(topics, on = 'topic_id')

    # Filter DataFrames
    filtered_merged_ent_t = merged_ent_t[merged_ent_t['course_id'].isin(course_ids)]
    entry_stats = filtered_merged_ent_t.groupby('entry_posted_by_user_id').agg(
    num_entries=('entry_content', 'count'),
    num_topics=('topic_id', 'nunique')
    ).reset_index()

    # Further merge to get stats
    students = merged_e_c_u[merged_e_c_u['course_code'].isin(instructor_courses)][
        ['user_id', 'user_name', 'semester','course_code']
    ]
    students_with_stats = students.merge(
        entry_stats,
        left_on='user_id',
        right_on='entry_posted_by_user_id',
        how='left'
    )

    # Fill empty entries with 0 to filter below
    students_with_stats[['num_entries', 'num_topics']] = students_with_stats[['num_entries', 'num_topics']].fillna(0).astype(int)

    # Extract stats
    at_risk_students = students_with_stats[
        students_with_stats['num_entries'] == 0
    ][['user_id', 'user_name', 'course_code','num_entries']]
    at_risk_total = at_risk_students['course_code'].value_counts().to_dict()

    return AtRiskResponse(
    at_risk_students=at_risk_students.to_dict(orient='records'),
    at_risk_total=at_risk_total
    )


