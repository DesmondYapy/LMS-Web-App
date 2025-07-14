# LMS Discussion Analytics Web Application

## 📌 Project Purpose

This project is a **fully functional web application** designed to provide **intuitive and useful instructor-facing interfaces**, enabling instructors to **gain actionable insights into student participation**. It helps instructors **view, explore, and understand discussion activity** within a Learning Management System (LMS).

By offering detailed analytics on **student engagement**, **discussion board activity**, and **course participation**, this tool aims to make it easier for educators to **identify at-risk students**, **highlight top contributors**, and **monitor overall class interaction**.


## 🛠️ Tech Stack

### Frontend: Python Streamlit
- Built using **Streamlit** to **rapidly prototype and visualize interactive dashboards**.
- Streamlit provides a **fast and easy-to-use** framework ideal for Proof-of-Concept (PoC) development.
- **Future scope**: When the project matures, it can be migrated to a more robust frontend like **React** for greater customizability and scalability.

### Backend: Python FastAPI
- Built with **FastAPI** for its:
    - **Intuitive syntax** and easy-to-use API routing.
    - **Automatic interactive API documentation** with **Swagger UI** (`/docs`).
    - **High performance**, built on **Starlette** and **Pydantic** for speed and data validation.
    - **Asynchronous support** enabling future scalability for high-volume data processing.


## 📦 Requirements

- **Docker**: Ensure **Docker** is installed and running on your machine.  
[Get Docker](https://www.docker.com/products/docker-desktop/)


## 🚀 How to Run the Project

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/LMS-Web-App.git
    ```

2. **Navigate to the project directory**
    ```bash
    cd Standard_Web_App
    ```

3. **Build the Docker image**
    ```bash
    docker build -t lms-web-app .
    ```

4. **Run the Docker container**
    ```bash
    docker run -p 8000:8000 -p 8501:8501 lms-web-app
    ```

- **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)  
- **Frontend Dashboard**: [http://localhost:8501](http://localhost:8501)


### ✅ Default Login Credentials

**Instructor Account**  
- Email: `instructor@test.com`  
- Password: `instructor123`

**Admin Account**  
- Email: `admin@test.com`  
- Password: `admin123`


## 📁 Project Structure

### Main Project Folder: `LMS-Web-App/`

- **`Backend/`**
  - `models/` – Contains all API request, response models, and database models for clean, maintainable, and organized code.
  - `raw_data/` – Stores raw data files (Excel format) used in the project.
  - `routes/` – Contains all FastAPI route files.
  - `utils/` – Helper functions including data loading utilities and `db.py` for database initialization.
  - `main.py` – Main FastAPI backend application that ties everything together.
  - `seed.py` – Script to create instructor and admin accounts on startup.

- **`Frontend/`**
  - `admin/` – Contains Streamlit pages and logic related to admin views.
  - `images/` – Folder for storing images to be used in the frontend (e.g., logo), currently empty.
  - `instructor/` – Streamlit pages and logic specific to instructor views.
  - `utils/` – Helper functions for calling backend API 
  - `app.py` – Main Streamlit app that ties together all frontend components.
  - `Data_View.py` – Standalone Streamlit page for viewing raw data files.
  - `settings.py` – Placeholder for settings page, currently empty.

- **.gitignore** – Specifies files and directories to exclude from version control.
- **Dockerfile** – Dockerfile to containerize both backend and frontend services.
- **entrypoint.sh** – Shell script to start both backend and frontend servers in Docker and run `seed.py` on startup.
- **README.md** – Main project documentation file.


## ✅ Future TODO List

- [ ] Add **API middleware** for security/authentication.
- [ ] Implement **API dependencies** for better modularization.
- [ ] Add **type checking** for helper functions.
- [ ] Abstract **student search logic** into backend API for cleaner frontend code.
- [ ] Complete the **settings page** in the frontend.
- [ ] Clean and enhance **admin-specific features**.
- [ ] Add images for logo
- [ ] Implement caching in frontend for faster response times



## 🗂️ Data Description

| **Table**      | **Description**                                                                 |
|----------------|---------------------------------------------------------------------------------|
| **courses**    | Stores information about courses available in the LMS.                          |
| **topics**     | Contains data about discussion topics posted within courses.                    |
| **entries**    | Stores individual posts or comments under each discussion topic.                |
| **users**      | Stores user information such as student or instructor details.                  |
| **enrollments**| Captures which users are enrolled in which courses.                             |
| **login**      | Stores login credentials and associated login IDs for each user in the system.  |


