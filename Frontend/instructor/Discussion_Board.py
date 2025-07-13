import requests
import pandas as pd 
import numpy as np
import streamlit as st

st.title("Discussion Board")
instructor_courses = ['TEK102','IHU224','LOH116'] # Hardcoded these but it should be via GET request with instructor ID

courses = pd.read_excel("../Backend/data tables/courses.xlsx")
enrollment = pd.read_excel("../Backend/data tables/enrollment.xlsx")
entries = pd.read_excel("../Backend/data tables/entries.xlsx")
login = pd.read_excel("../Backend/data tables/login.xlsx")
topics = pd.read_excel("../Backend/data tables/topics.xlsx")
users = pd.read_excel("../Backend/data tables/users.xlsx")

st.header("COURSES YOU ARE TEACHING")
tab1, tab2, tab3 = st.tabs(instructor_courses)    

with tab1:
    course_code = instructor_courses[0]

    merged_entries_topic = topics \
        .merge(entries, on="topic_id", how="left") \
        .merge(courses, on="course_id", how="left")    

    merged_entries_topic['entry_created_at'] = pd.to_datetime(merged_entries_topic['entry_created_at'])

    merged_user = merged_entries_topic.merge(
            users,
            left_on='entry_posted_by_user_id',
            right_on='user_id',
            how='left'
        )

    filtered = merged_user[merged_user['course_code'] == course_code]
    filtered = filtered[['topic_id', 'topic_title', 'topic_content', 'entry_content', 'entry_created_at', 'user_name']]
    grouped = filtered.sort_values('entry_created_at').groupby(['topic_id', 'topic_title','topic_content'])


    for (topic_id, topic_title, topic_content), group in grouped:
        st.subheader(f"📝 Topic: {topic_title} ({topic_id})")
        st.caption(f"Content: {topic_content}")
        # Generate a list of markdown strings for each entry
        markdown_entries = []
        for _, row in group.iterrows():
            md = f"""
            - **Posted by**: `{row['user_name']}`  
            - **When**: {row['entry_created_at'].strftime('%Y-%m-%d %H:%M')}  
            - **Content**:  
                > {row['entry_content']}
            """
            markdown_entries.append(md)

        # Display entries in rows of 3 columns
        for i in range(0, len(markdown_entries), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(markdown_entries):
                    with cols[j]:
                        st.markdown(markdown_entries[i + j])
