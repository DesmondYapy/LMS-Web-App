from fastapi import FastAPI
from routes import auth, courses, students, overview, discussion_board

app = FastAPI()

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(overview.router)
app.include_router(students.router)
app.include_router(discussion_board.router)

