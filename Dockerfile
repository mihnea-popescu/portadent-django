# Use an official Python 3.9.6 image as the base image
FROM python:3.9.6-slim

# Set environment variables to prevent Python from writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required by psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the entire project to the container's working directory
COPY . /app/

# Expose the port on which Django will run (default is 8000)
EXPOSE 8000

# Run Gunicorn instead of Django's development server
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]