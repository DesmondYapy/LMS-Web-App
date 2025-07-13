import streamlit as st
import pandas as pd

st.header("Raw Data View")

courses = pd.read_excel("../Backend/data tables/courses.xlsx")
enrollment = pd.read_excel("../Backend/data tables/enrollment.xlsx")
entries = pd.read_excel("../Backend/data tables/entries.xlsx")
login = pd.read_excel("../Backend/data tables/login.xlsx")
topics = pd.read_excel("../Backend/data tables/topics.xlsx")
users = pd.read_excel("../Backend/data tables/users.xlsx")

st.subheader('Courses')
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