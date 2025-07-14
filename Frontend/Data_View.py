import streamlit as st
import pandas as pd

st.header("Raw Data View")

courses = pd.read_excel("../Backend/raw_data/courses.xlsx")
enrollment = pd.read_excel("../Backend/raw_data/enrollment.xlsx")
entries = pd.read_excel("../Backend/raw_data/entries.xlsx")
login = pd.read_excel("../Backend/raw_data/login.xlsx")
topics = pd.read_excel("../Backend/raw_data/topics.xlsx")
users = pd.read_excel("../Backend/raw_data/users.xlsx")

st.subheader("Courses")
st.write(courses)
st.subheader("Enrollment")
st.write(enrollment)
st.subheader("Entries")
st.write(entries)
st.subheader("Login")
st.write(login)
st.subheader("Topic")
st.write(topics)
st.subheader("Users")
st.write(users)
