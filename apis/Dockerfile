# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install  -r requirements.txt

# Copy the FastAPI code
COPY . .

# Command to run FastAPI
CMD ["fastapi", "dev", "provide_sim.py", "--host", "0.0.0.0", "--port", "5000"]
