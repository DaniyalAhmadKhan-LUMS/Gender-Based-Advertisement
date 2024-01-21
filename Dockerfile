# Use Python 3.9 as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Install CMake (and other necessary system dependencies if any)
RUN apt-get update && apt-get install -y cmake
RUN apt-get update && apt-get install -y nano
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Set the DISPLAY environment variable for GUI applications
ENV DISPLAY=:0

# Copy the age-and-gender folder into the container
COPY age-and-gender ./age-and-gender

# Install required Python packages
RUN pip install numpy face_recognition opencv-python

# Build and install the age-and-gender repository
RUN cd age-and-gender && python setup.py install

# Command to run the Python script
CMD ["python", "./age-and-gender/example/example_live.py"]

