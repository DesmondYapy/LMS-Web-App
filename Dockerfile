FROM python:3.11-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY Backend /app/Backend
COPY Frontend /app/Frontend

# Seed database
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000 8501

CMD ["/app/entrypoint.sh"]
