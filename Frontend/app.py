# frontend.py
import streamlit as st
import requests

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Admin", "Instructor"]

def login():
    # Login form
    st.header("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
    
        if st.form_submit_button('Login'):

            response = requests.post("http://localhost:8000/login", json={
                "email": email,
                "password": password
            })
            if response.status_code == 200:
                token = response.json()['access_token']
                role = response.json()['role']
                st.success(f"Welcome, {role}!")
                st.session_state['token'] = token
                st.session_state.role = role
                st.code(response.json(),height='content',wrap_lines=True)
                st.rerun()
            else:
                st.error("Invalid credentials")

def logout():
    st.session_state.role = None
    st.rerun()

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
data_view = st.Page("Data_View.py", title="Raw Data View")

dashboard = st.Page(
    "instructor/Dashboard.py",
    title="Dashboard",
    icon=":material/help:",
    default=(st.session_state.role == "instructor"),
)

discussion_board = st.Page(
    "instructor/Discussion_Board.py",
    title="Discussion Board",
    icon=":material/help:",
)

student_search = st.Page(
    "instructor/Student_Search.py",
    title="Student Search",
    icon=":material/help:",
)


admin_dashboard = st.Page(
    "admin/Dashboard.py",
    title="Dashboard",
    icon=":material/help:",
    default=(st.session_state.role == "admin"),
)

admin_discussion_board = st.Page(
    "admin/Discussion_Board.py",
    title="Discussion Board",
    icon=":material/help:",
)

admin_student_search = st.Page(
    "admin/Student_Search.py",
    title="Student Search",
    icon=":material/help:",
)

account_pages = [logout_page, settings]
instructor_pages = [dashboard, discussion_board, student_search]
admin_pages = [admin_dashboard, admin_discussion_board, admin_student_search]

st.title("LMS Discussion Viewer")
# st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

page_dict = {}

if st.session_state.role == "instructor":
    page_dict["instructor"] = instructor_pages
if st.session_state.role == "admin":
    page_dict["admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict | {"Data":[data_view]} )

else:
    pg = st.navigation([st.Page(login)])
    
pg.run()


