import pandas as pd 
import streamlit as st

from utils.api_calls import get_instructor_course, get_discussion_board

instructor_courses = get_instructor_course()

# Start of FE
st.title("Discussion Board")
st.header("Courses You Are Teaching")

tab_labels = [f"{course}" for course in instructor_courses]
tabs = st.tabs(tab_labels)

# Display of discussion board in tabs
for i, course_code in enumerate(instructor_courses):
    with tabs[i]:

        topics = get_discussion_board(course_code)
        
        if not topics:
            st.info("No discussion topics available.")
            continue

        for topic in topics:
            st.subheader(f"📝 Topic: {topic['topic_title']} ({topic['topic_id']})")
            st.caption(f"Content: {topic['topic_content']}")

            entries = topic.get('entries', [])

            if not entries:
                st.write("No entries posted yet.")
                continue

            # Entries markdown formatting
            markdown_entries = []
            for entry in entries:
                entry_created_at = pd.to_datetime(entry['entry_created_at']).strftime('%Y-%m-%d %H:%M')
                md = f"""
                - **Posted by**: `{entry['user_name']}`  
                - **When**: {entry_created_at}  
                - **Content**:  
                    > {entry['entry_content']}
                """
                markdown_entries.append(md)

            # Display entries in rows of 3 columns
            for j in range(0, len(markdown_entries), 3):
                cols = st.columns(3)
                for k in range(3):
                    if j + k < len(markdown_entries):
                        with cols[k]:
                            st.markdown(markdown_entries[j + k])