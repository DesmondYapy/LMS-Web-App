# frontend.py
import requests
import pandas as pd 
import numpy as np
import streamlit as st

st.title("Dashboard")

def get_instructor_course():
    response = requests.post("http://localhost:8000/instructor-courses", json={
        "instructor_id": 0,
        "role": "instructor"
        })

    if response.status_code == 200:
        instructor_courses = response.json()['instructor_courses']
        return instructor_courses
    else:
        return []

def get_overview_stats(instructor_courses):
    response = requests.post("http://localhost:8000/overview-stats", json={
    "instructor_courses": instructor_courses,
    })

    if response.status_code == 200:
        total_topics = response.json()['total_topics']
        total_students = response.json()['total_students']
        total_entries = response.json()['total_entries']
        topic_counts = response.json()['topic_counts']

        return total_topics,total_students,total_entries,topic_counts
    
    else:
        return []

def get_at_risk(instructor_courses):
    response = requests.post("http://localhost:8000/at-risk", json={
    "instructor_courses": instructor_courses,
    })

    if response.status_code == 200:
        at_risk_students = response.json()['at_risk_students']
        at_risk_total = response.json()['at_risk_total']

        return at_risk_students, at_risk_total
    
    else:
        return []

def get_course_stats(course_code):
    response = requests.post("http://localhost:8000/course-stats", json={
    "course_code": course_code,
    })

    if response.status_code == 200:
        total_topics=response.json()['total_topics']
        total_students=response.json()['total_students']
        total_entries=response.json()['total_entries']
        entries_per_topic=response.json()['entries_per_topic']
        weekly_topic_counts=response.json()['weekly_topic_counts']
    
        return total_topics, total_students, total_entries, entries_per_topic, weekly_topic_counts
    
    else:
        return []
    
courses = pd.read_excel("../Backend/raw_data/courses.xlsx")
enrollment = pd.read_excel("../Backend/raw_data/enrollment.xlsx")
entries = pd.read_excel("../Backend/raw_data/entries.xlsx")
login = pd.read_excel("../Backend/raw_data/login.xlsx")
topics = pd.read_excel("../Backend/raw_data/topics.xlsx")
users = pd.read_excel("../Backend/raw_data/users.xlsx")

st.header("COURSES YOU ARE TEACHING")

instructor_courses = get_instructor_course()
tab_labels = ["📊 Overview"] + get_instructor_course()

tabs = st.tabs(tab_labels)

merged_entries_topic = topics \
    .merge(entries, on="topic_id", how="left") \
    .merge(courses, on="course_id", how="left")

merged_enroll_course = enrollment.merge(courses, on="course_id")

# Overview Tab
with tabs[0]:
    st.header("📊 All Courses")
    total_topics,total_students,total_entries,topic_counts = get_overview_stats(instructor_courses)
    at_risk_students, at_risk_total = get_at_risk(instructor_courses)
    
    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric('Total topics',total_topics)
    with col2:
        st.metric('Total Students',total_students)
    with col3:
        st.metric('Total Entries', total_entries)

    st.bar_chart(topic_counts, y_label="Number of Topics", x_label="Course Title")

    st.subheader("🚨 At-Risk Students (No Entries Made)")
    
    cols = st.columns(3)

    for idx, (course_code, count) in enumerate(at_risk_total.items()):
        col = cols[idx % 3]
        with col:
            st.metric(course_code, f"{count} students")

        # Start a new row of columns after every 3 metrics
        if (idx + 1) % 3 == 0:
            cols = st.columns(3)

    st.write(pd.DataFrame(at_risk_students).sort_values(['course_code','num_entries','user_id']))

# Course Specific Tabs
for i, course_code in enumerate(instructor_courses, start=1):
    with tabs[i]:
        total_topics, total_students, total_entries, entries_per_topic, weekly_topic_counts = get_course_stats(course_code)
        
        col1,col2,col3 = st.columns(3)
        with col1:
            st.metric('Total topics',total_topics)
        with col2:
            st.metric('Total Students',total_students)
        with col3:
            st.metric('Total Entries', total_entries)
    
        st.subheader("Entries per Topic")
        st.bar_chart(entries_per_topic, y_label="Number of Entries", x_label="Topic Title")
        
        st.subheader("Weekly Entry Count per Topic")
        line_chart_data = pd.DataFrame.from_dict(weekly_topic_counts, orient='index')
        line_chart_data.index = pd.to_datetime(line_chart_data.index)  # Optional: make index datetime for nicer chart
        line_chart_data = line_chart_data.sort_index()

        st.line_chart(line_chart_data)



tab1,tab2,tab3,tab4 = st.tabs(tab_labels)

with tab1:
    st.header("DONE")



with tab2:
    # st.title(f'{instructor_courses[0]}: {courses[courses["course_code"]==instructor_courses[0]]['course_name']}')
    st.title('WEB DEVELOPMENT')
    course_code = instructor_courses[0]
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


    st.subheader("Top 3 Students")
    top3_students = students_with_stats[['user_id', 'user_name', 'num_entries', 'num_topics']] \
        .sort_values(['num_topics', 'num_entries', 'user_id'], ascending=[False, False, True])\
        .head(3)\

    cols = st.columns(3)

    for i, (_, row) in enumerate(top3_students.iterrows()):
        with cols[i]:
            st.metric("👤 Student", row['user_name'])
            st.metric("📝 Entries", row['num_entries'])
            st.metric("📚 Unique Topics", row['num_topics'])

    st.subheader("List of Students")
    st.write(
        students_with_stats[['user_id', 'user_name', 'semester', 'num_entries', 'num_topics']]
        .sort_values(['num_topics', 'num_entries', 'user_id'], ascending=[False, False, True])
    )



# with tab3:
#     # st.title(f'{instructor_courses[0]}: {courses[courses["course_code"]==instructor_courses[0]]['course_name']}')
#     st.title('BUSINESS ANALYTICS')
#     course_code = instructor_courses[2]
#     total_topics = merged_entries_topic[
#         merged_entries_topic['course_code'] == course_code
#         ]['topic_title'].nunique()
    
#     total_students = merged_enroll_course[
#         (merged_enroll_course['course_code'] == course_code) &
#         (merged_enroll_course['enrollment_state'] == 'active')
#     ]['user_id'].nunique()

#     total_entries = merged_entries_topic[
#         merged_entries_topic['course_code'] == course_code
#         ]['entry_id'].nunique()

#     col1,col2,col3 = st.columns(3)
#     with col1:
#         st.metric('Total topics',total_topics)
#     with col2:
#         st.metric('Total Students',total_students)
#     with col3:
#         st.metric('Total Entries', total_entries)


# with tab4:
#     # st.title(f'{instructor_courses[0]}: {courses[courses["course_code"]==instructor_courses[0]]['course_name']}')
#     st.title('SOCIAL WORK')
#     course_code = instructor_courses[3]
#     total_topics = merged_entries_topic[
#         merged_entries_topic['course_code'] == course_code
#         ]['topic_title'].nunique()
    
#     total_students = merged_enroll_course[
#         (merged_enroll_course['course_code'] == course_code) &
#         (merged_enroll_course['enrollment_state'] == 'active')
#     ]['user_id'].nunique()

#     total_entries = merged_entries_topic[
#         merged_entries_topic['course_code'] == course_code
#         ]['entry_id'].nunique()

#     col1,col2,col3 = st.columns(3)
#     with col1:
#         st.metric('Total topics',total_topics)
#     with col2:
#         st.metric('Total Students',total_students)
#     with col3:
#         st.metric('Total Entries', total_entries)