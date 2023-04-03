# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Update the package list and install FFmpeg
RUN apt-get update && \
	apt-get install -y ffmpeg

# Copy the requirements.txt file into the container
COPY app/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container
COPY app/ .

# Expose the port your application will run on, for example 8080
EXPOSE 8080

# Define the command to run your application
CMD ["python", "server.py"]
