from fastapi import FastAPI
from routes import auth, courses, students, topics, overview

app = FastAPI()

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(overview.router)
app.include_router(students.router)
app.include_router(topics.router)

