# Use official Python slim image
FROM python:3.10.8-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run both gunicorn and main.py
CMD ["bash", "-c", "gunicorn app:app & python3 main.py"]
