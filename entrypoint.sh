#!/bin/sh

# Run seed.py to create instructor and admin accounts
cd /app/Backend
echo "Seeding database..."
python seed.py

# Start backend (port 8000) and frontend (port 8501) in background
echo "Starting Backend on port 8000..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

echo "Starting Frontend (Streamlit) on port 8501..."
cd /app/Frontend
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
