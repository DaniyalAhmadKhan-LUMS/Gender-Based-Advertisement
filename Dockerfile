# Use an ARM compatible Python base image if necessary
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Install CMake and other dependencies
RUN apt-get update && apt-get install -y cmake nano libgl1-mesa-glx

# Install OpenCV Python (headless version)
RUN pip install numpy face_recognition opencv-python-headless

# Copy the age-and-gender folder into the container
COPY age-and-gender ./age-and-gender

# Build and install the age-and-gender repository
RUN cd age-and-gender && python setup.py install

# Command to run the Python script
CMD ["python", "./age-and-gender/example/example_live.py"]

