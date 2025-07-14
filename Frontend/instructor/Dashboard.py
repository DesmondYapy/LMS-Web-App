# frontend.py
import requests
import pandas as pd 
import numpy as np
import streamlit as st

st.title("Dashboard")

## API Calling Functions
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
        course_name=response.json()['course_name']
        total_topics=response.json()['total_topics']
        total_students=response.json()['total_students']
        total_entries=response.json()['total_entries']
        entries_per_topic=response.json()['entries_per_topic']
        weekly_topic_counts=response.json()['weekly_topic_counts']
    
        return course_name, total_topics, total_students, total_entries, entries_per_topic, weekly_topic_counts
    
    else:
        return []

def get_top_students(course_code):
    response = requests.post("http://localhost:8000/top-students", json={
    "course_code": course_code,
    })

    if response.status_code == 200:
        top_3_students=response.json()['top_3_students'],
        list_of_students=response.json()['list_of_students']
    

        top_3_students = pd.DataFrame(top_3_students[0])
        list_of_students = pd.DataFrame(list_of_students)

        return top_3_students, list_of_students
    
    else:
        return []
    


## Start of FE
instructor_courses = get_instructor_course()

st.header("Courses You Are Teaching")
tab_labels = ["📊 Overview"] + get_instructor_course()
tabs = st.tabs(tab_labels)


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

        # Course Specific Stats
        course_name, total_topics, total_students, total_entries, entries_per_topic, weekly_topic_counts = get_course_stats(course_code)

        st.title(course_name.upper())
        
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
        line_chart_data.index = pd.to_datetime(line_chart_data.index)
        line_chart_data = line_chart_data.sort_index()

        st.line_chart(line_chart_data)

        # Top 3 Students
        top_3_students, list_of_students = get_top_students(course_code)
        
        st.subheader("Top 3 Students")

        cols = st.columns(3)

        for i, (_, row) in enumerate(top_3_students.iterrows()):
            with cols[i]:
                st.metric("👤 Student", row['user_name'])
                st.metric("📝 Entries", row['num_entries'])
                st.metric("📚 Unique Topics", row['num_topics'])

        st.subheader("List of Students")
        st.write(list_of_students)