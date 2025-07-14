import pandas as pd 

from fastapi import APIRouter, Depends, HTTPException

from models.request import TopStudentsRequest
from models.response import TopStudentsResponse

from utils.data_loader import topics, entries, courses, enrollments, users

router = APIRouter()

@router.post("/top-students", response_model = TopStudentsResponse)
def get_top_3_students(data: TopStudentsRequest) -> TopStudentsResponse:

    """
    Returns the top 3 students in a course
    """

    course_code = data.course_code
    course_id = courses[courses['course_code']==course_code]['course_id'].iloc[0]


    # Merge DataFrames
    merged_e_c_u = enrollments \
        .merge(courses, on='course_id') \
        .merge(users, on='user_id')
    merged_ent_t = entries \
        .merge(topics, on='topic_id')
    
    # Filter DataFrame
    filtered_merged_e_c_u = merged_e_c_u[
        merged_e_c_u['course_code']==course_code
        ]
    filtered_merged_ent_t = merged_ent_t[
        merged_ent_t['course_id'] == course_id
        ]
    
    # Data Manipulation
    entry_stats = filtered_merged_ent_t \
        .groupby('entry_posted_by_user_id') \
        .agg(
            num_entries=('entry_content', 'count'),
            num_topics=('topic_id', 'nunique')) \
        .reset_index()
    students = filtered_merged_e_c_u[
        ['user_id', 'user_name', 'semester']
    ]
    students_with_stats = students.merge(
        entry_stats,
        left_on='user_id',
        right_on='entry_posted_by_user_id',
        how='left'
    )
    students_with_stats[['num_entries', 'num_topics']] = students_with_stats[
        ['num_entries', 'num_topics']] \
            .fillna(0) \
            .astype(int)
    
    # Extract Stats
    top_3_students = students_with_stats[['user_id', 'user_name', 'semester', 'num_entries', 'num_topics']] \
        .sort_values(['num_topics', 'num_entries', 'user_id'], ascending=[False, False, True])\
        .head(3)
    
    list_of_students = students_with_stats[
        ['user_id', 'user_name', 'semester', 'num_entries', 'num_topics']] \
            .sort_values(['num_topics', 'num_entries', 'user_id'], 
                         ascending=[False, False, True])
    
    top_3_students = top_3_students.to_dict(orient='records')
    list_of_students = list_of_students.to_dict(orient='records')


    return TopStudentsResponse(
        top_3_students=top_3_students,
        list_of_students=list_of_students
    )