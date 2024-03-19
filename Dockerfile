# Use an official Python runtime as a parent image
FROM python:3.9.6-slim

# Set the working directory in the container
WORKDIR /usr/src/jobapplicationmanager

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN apt-get update -y
RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5001

# Define environment variable
#ENV NAME xxx

# Run app.py when the container launches
CMD ["python", "./run.py"]

