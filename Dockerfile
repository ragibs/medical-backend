# Use a minimal Python image for lightweight setup
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for MySQL client
RUN apk update && apk add --no-cache \
    mariadb-connector-c-dev gcc musl-dev bash

# Copy requirements.txt and install Python dependencies
COPY requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

# Copy wait-for-it.sh script and make it executable
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Copy the Django application code into the container
COPY . /app

# Set essential environment variables
ENV DJANGO_SETTINGS_MODULE=MedAppBackend.settings
ENV PYTHONUNBUFFERED=1

# Expose the Django development server port
EXPOSE 8000

## Run database migrations and then start the Django development server
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
