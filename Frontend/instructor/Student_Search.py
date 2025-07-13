# frontend.py
import requests
import pandas as pd 
import numpy as np
import streamlit as st

st.header("Student Look-up")
instructor_courses = ['TEK102', 'IHU224', 'LOH116']  # Ideally fetched via GET with instructor ID
colors = ["blue", "green", "orange", "red", "violet", "gray"]
markdown = ""
for i, course in enumerate(instructor_courses):
    markdown += f" :{colors[i]}-badge[{course}]"
st.markdown(markdown)

courses = pd.read_excel("../Backend/raw_data/courses.xlsx")
enrollment = pd.read_excel("../Backend/raw_data/enrollment.xlsx")
entries = pd.read_excel("../Backend/raw_data/entries.xlsx")
login = pd.read_excel("../Backend/raw_data/login.xlsx")
topics = pd.read_excel("../Backend/raw_data/topics.xlsx")
users = pd.read_excel("../Backend/raw_data/users.xlsx")


merged_entries_topic = topics \
    .merge(entries, on="topic_id", how="left") \
    .merge(courses, on="course_id", how="left")


merged_enroll_course = enrollment.merge(courses, on="course_id")

if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "data" not in st.session_state:
    st.session_state.data = None

with st.form("student-look-up-form"):
    user_name = st.text_input("Student User Name")
    st.session_state.user_name = user_name

    
    if st.form_submit_button('Search'):
        filtered = users[users["user_name"] == user_name]
        if filtered.empty:
            st.error(f"No user found with name {user_name}")
            st.session_state['user_name'] = ''
            
        else:
            user_id = filtered['user_id'].iloc[0]
            st.session_state.user_id = user_id

            total_topics = merged_entries_topic[
                merged_entries_topic['topic_posted_by_user_id'] == user_id
                ]['topic_title'].nunique()


            total_entries = merged_entries_topic[
                merged_entries_topic['entry_posted_by_user_id'] == user_id
                ]['entry_id'].nunique()
        
            col1,col2,col3 = st.columns(3)
            
            with col1:
                st.metric("User ID", user_id)
            with col2:
                st.metric("Topics Posted",total_topics)
            with col3:
                st.metric("Entries Made",total_entries)

            merged_entries_topic['entry_created_at'] = pd.to_datetime(merged_entries_topic['entry_created_at'], errors='coerce')
            merged_entries_topic = merged_entries_topic.dropna(subset=['entry_created_at'])
            merged_entries_topic['week'] = merged_entries_topic['entry_created_at'].dt.to_period('W').apply(lambda r: r.start_time)
            st.session_state.data = merged_entries_topic

            # Show stats per course for the selected user
            for course in instructor_courses:
                with st.expander(f"{course}"):
                    # Filter for this course and user
                    user_entries = merged_entries_topic[
                        (merged_entries_topic['course_code'] == course) &
                        (merged_entries_topic['entry_posted_by_user_id'] == user_id)
                    ]

                    # Entries per topic
                    entries_per_topic = user_entries['topic_title'].value_counts().sort_index()

                    st.subheader(f"{user_name}'s Entries per Topic")
                    st.bar_chart(entries_per_topic, y_label="Number of Entries", x_label="Topic Title")

                    # Weekly entry count per topic (for this course)
                    weekly_topic_counts = merged_entries_topic[
                        (merged_entries_topic['course_code'] == course) &
                        (merged_entries_topic['entry_posted_by_user_id'] == user_id)
                    ].groupby(['week', 'topic_title']).size().reset_index(name='num_entries')

                    pivot_df = weekly_topic_counts.pivot(index='week', columns='topic_title', values='num_entries').fillna(0)
                    pivot_df = pivot_df.sort_index()

                    st.subheader("Weekly Entry Count per Topic")
                    st.line_chart(pivot_df)
                    st.write(weekly_topic_counts)

    
if len(st.session_state.user_name) >0:
    with st.expander(f"Raw File for Student: {st.session_state.user_name}"):

            file = merged_entries_topic[
                    (merged_entries_topic['course_code'].isin(instructor_courses)) &
                    (merged_entries_topic['entry_posted_by_user_id'] == st.session_state.user_id)
                ]
            
            st.write(file)
            
            st.download_button(
                label="Download",
                data=file.to_csv().encode("utf-8"),
                file_name="data.csv",
                mime="text/csv",
                icon=":material/download:",
                )
                    
            # response = requests.post("http://localhost:8000/login", json={
            #     "email": email,
            #     "password": password
            # })
            # if response.status_code == 200:
            #     token = response.json()['access_token']
            #     role = response.json()['role']
            #     st.success(f"Welcome, {role}!")
            #     st.session_state['token'] = token
            #     st.session_state.role = role
            #     st.code(response.json(),height='content',wrap_lines=True)
            #     st.rerun()
            # else:
            #     st.error("Invalid credentials")