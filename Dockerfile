# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Remove build dependencies
RUN apt-get purge -y build-essential
RUN rm -r /root/.cache/pip

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable

# Run app.py when the container launches
CMD ["gunicorn", "--bind=0.0.0.0:5000", "app"]
