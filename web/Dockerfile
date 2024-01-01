# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install OpenCV and other dependencies
RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY ./app .
COPY ./requirements.txt .
COPY ./entrypoint.sh /entrypoint.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Make entrypoint.sh executable
RUN chmod +x /entrypoint.sh

# Define environment variable
ENV PYTHONDONTWRITEBYTECODE 1

# Use entrypoint.sh to start the app
ENTRYPOINT ["/entrypoint.sh"]
