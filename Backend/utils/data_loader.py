# app/data_loader.py
import pandas as pd

courses = pd.read_excel("raw_data/courses.xlsx")
topics = pd.read_excel("raw_data/topics.xlsx")
entries = pd.read_excel("raw_data/entries.xlsx")
users = pd.read_excel("raw_data/users.xlsx")
enrollments = pd.read_excel("raw_data/enrollment.xlsx")
