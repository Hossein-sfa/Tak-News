# Use a base image with Python installed
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install required packages including PostgreSQL server and Redis
RUN apt-get update && apt-get install -y postgresql postgresql-contrib redis-server 

# Update pip
RUN pip install --upgrade pip

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the container
COPY . .
