# Use the official Python image from the Docker Hub
FROM python:3.8.5-slim

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Make a new directory to put our code in.
RUN mkdir /code

# Change the working directory. 
# Every command after this will be run from the /code directory.
WORKDIR /code

# Copy the of the code. 
COPY . /code/

# Add sqlite3 to enable dbshell command for managing the database
RUN apt-get update -y && apt-get install sqlite3 -y

# Upgrade pip
RUN pip install --upgrade pip

# Install the requirements.
RUN pip install -r requirements.txt

# Import groupid environment variable
ENV GROUPID=${GROUPID}

# Copy start script
COPY start.sh /usr/local/bin/start.sh

# Run start script (database migrate and start)
CMD ["/bin/bash", "/usr/local/bin/start.sh"]
