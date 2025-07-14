## API Calling Functions
import requests
import pandas as pd

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
    
def get_discussion_board(course_code):
    response = requests.post("http://localhost:8000/discussion-board", json={
    "course_code": course_code,
    })

    if response.status_code == 200:
        topics = response.json()['topics']
        
        return topics
    
    else:
        return []
    