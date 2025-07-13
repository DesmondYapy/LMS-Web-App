# frontend.py
import requests
import pandas as pd 
import numpy as np
import streamlit as st

st.title("Dashboard")

instructor_courses = ['TEK102','IHU224','LOH116'] # Hardcoded these but it should be via GET request with instructor ID

courses = pd.read_excel("../Backend/data tables/courses.xlsx")
enrollment = pd.read_excel("../Backend/data tables/enrollment.xlsx")
entries = pd.read_excel("../Backend/data tables/entries.xlsx")
login = pd.read_excel("../Backend/data tables/login.xlsx")
topics = pd.read_excel("../Backend/data tables/topics.xlsx")
users = pd.read_excel("../Backend/data tables/users.xlsx")

st.header("COURSES YOU ARE TEACHING")
instructor_courses.insert(0,'Overview')
tab1, tab2, tab3, tab4 = st.tabs(instructor_courses)

merged_entries_topic = topics \
    .merge(entries, on="topic_id", how="left") \
    .merge(courses, on="course_id", how="left")

merged_enroll_course = enrollment.merge(courses, on="course_id")

with tab1:
    # st.title(f'{instructor_courses[0]}: {courses[courses["course_code"]==instructor_courses[0]]['course_name']}')
    st.title('All Courses')

    total_topics = merged_entries_topic[
    merged_entries_topic['course_code'].isin(instructor_courses)
]['topic_title'].nunique()

    total_students = merged_enroll_course[
        (merged_enroll_course['course_code'].isin(instructor_courses)) &
        (merged_enroll_course['enrollment_state'] == 'active')
    ]['user_id'].nunique()

    total_entries = merged_entries_topic[
        merged_entries_topic['course_code'].isin(instructor_courses)
        ]['entry_id'].nunique()

    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric('Total topics',total_topics)
    with col2:
        st.metric('Total Students',total_students)
    with col3:
        st.metric('Total Entries', total_entries)

    merged_df = topics.merge(courses, on="course_id")
    topic_counts = merged_df[merged_df['course_code'].isin(instructor_courses)]['course_code'].value_counts().sort_index()
    st.subheader("Topics per Course")
    st.bar_chart(topic_counts, y_label="Number of Topics", x_label="Course Title")


with tab2:
    # st.title(f'{instructor_courses[0]}: {courses[courses["course_code"]==instructor_courses[0]]['course_name']}')
    st.title('WEB DEVELOPMENT')
    course_code = instructor_courses[1]
    total_topics = merged_entries_topic[
        merged_entries_topic['course_code'] == course_code
        ]['topic_title'].nunique()
    
    total_students = merged_enroll_course[
        (merged_enroll_course['course_code'] == course_code) &
        (merged_enroll_course['enrollment_state'] == 'active')
    ]['user_id'].nunique()

    total_entries = merged_entries_topic[
        merged_entries_topic['course_code'] == course_code
        ]['entry_id'].nunique()

    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric('Total topics',total_topics)
    with col2:
        st.metric('Total Students',total_students)
    with col3:
        st.metric('Total Entries', total_entries)

    entries_per_topic = merged_entries_topic[merged_entries_topic['course_code']==course_code]['topic_title'].value_counts().sort_index()
    st.subheader("Entries per Topic")
    st.bar_chart(entries_per_topic, y_label="Number of Entries", x_label="Topic Title")

    merged_entries_topic['entry_created_at'] = pd.to_datetime(merged_entries_topic['entry_created_at'])
    merged_entries_topic = merged_entries_topic.dropna(subset=['entry_created_at'])
    merged_entries_topic['week'] = merged_entries_topic['entry_created_at'].dt.to_period('W').apply(lambda r: r.start_time)
    weekly_topic_counts = merged_entries_topic[merged_entries_topic['course_code'] == course_code].groupby(['week', 'topic_title']).size().reset_index(name='num_entries')
    pivot_df = weekly_topic_counts.pivot(index='week', columns='topic_title', values='num_entries').fillna(0)
    pivot_df = pivot_df.sort_index()

    st.subheader("Weekly Entry Count per Topic")
    st.line_chart(pivot_df)


    # st.write(merged_entries_topic[merged_entries_topic['course_code']==course_code])
    st.subheader("List of Students")
    merged_enroll_course = merged_enroll_course.merge(users,on='user_id')

    # Merge entries with topics to get course_code per entry
    entries_with_course = entries.merge(topics, on='topic_id')
    entries_filtered = entries_with_course[entries_with_course['course_id'] == 23409]
    entry_stats = entries_filtered.groupby('entry_posted_by_user_id').agg(
    num_entries=('entry_content', 'count'),
    num_topics=('topic_id', 'nunique')
    ).reset_index()
    students = merged_enroll_course[merged_enroll_course['course_code'] == course_code][
        ['user_id', 'user_name', 'semester']
    ]

    students_with_stats = students.merge(
        entry_stats,
        left_on='user_id',
        right_on='entry_posted_by_user_id',
        how='left'
        )

    students_with_stats[['num_entries', 'num_topics']] = students_with_stats[['num_entries', 'num_topics']].fillna(0).astype(int)

    st.write(
        students_with_stats[['user_id', 'user_name', 'semester', 'num_entries', 'num_topics']]
        .sort_values(['num_topics', 'num_entries', 'user_id'], ascending=[False, False, True])
    )


with tab3:
    # st.title(f'{instructor_courses[0]}: {courses[courses["course_code"]==instructor_courses[0]]['course_name']}')
    st.title('BUSINESS ANALYTICS')
    course_code = instructor_courses[2]
    total_topics = merged_entries_topic[
        merged_entries_topic['course_code'] == course_code
        ]['topic_title'].nunique()
    
    total_students = merged_enroll_course[
        (merged_enroll_course['course_code'] == course_code) &
        (merged_enroll_course['enrollment_state'] == 'active')
    ]['user_id'].nunique()

    total_entries = merged_entries_topic[
        merged_entries_topic['course_code'] == course_code
        ]['entry_id'].nunique()

    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric('Total topics',total_topics)
    with col2:
        st.metric('Total Students',total_students)
    with col3:
        st.metric('Total Entries', total_entries)


with tab4:
    # st.title(f'{instructor_courses[0]}: {courses[courses["course_code"]==instructor_courses[0]]['course_name']}')
    st.title('SOCIAL WORK')
    course_code = instructor_courses[3]
    total_topics = merged_entries_topic[
        merged_entries_topic['course_code'] == course_code
        ]['topic_title'].nunique()
    
    total_students = merged_enroll_course[
        (merged_enroll_course['course_code'] == course_code) &
        (merged_enroll_course['enrollment_state'] == 'active')
    ]['user_id'].nunique()

    total_entries = merged_entries_topic[
        merged_entries_topic['course_code'] == course_code
        ]['entry_id'].nunique()

    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric('Total topics',total_topics)
    with col2:
        st.metric('Total Students',total_students)
    with col3:
        st.metric('Total Entries', total_entries)