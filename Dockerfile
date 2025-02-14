# Use the official Python image
FROM python:3.9-slim

# Prevent Python from generating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG VERSION
LABEL version=$VERSION

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY /src/* /app/
COPY requirements.txt /app

# Install any required Python dependencies
RUN pip install -r requirements.txt

# Install cron in the container
RUN apt-get update && apt-get install -y cron

# Copy the crontab file into the container
COPY crontab /etc/cron.d/mycron

# Give execute permissions on the cron job
RUN chmod 0644 /etc/cron.d/mycron
RUN chmod +x /etc/cron.d/mycron

# Apply the cron job
RUN crontab /etc/cron.d/mycron

# Start the cron service
CMD ["cron", "-f"]