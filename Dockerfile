# Use dustynv/opencv:4.8.1-r36.2.0 as the base image
FROM dustynv/opencv:4.8.1-r36.2.0

# Set the working directory in the container
WORKDIR /usr/src/app

# Install CMake, Nano, libgl1-mesa-glx, libpng-dev, and add libjpeg-dev for JPEG support
RUN apt-get update && apt-get install -y \
    cmake \
    nano \
    libgl1-mesa-glx \
    libpng-dev \
    libjpeg-dev \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir numpy face_recognition

# Copy the age-and-gender folder into the container
COPY age-and-gender ./age-and-gender

# Build and install the age-and-gender repository
RUN cd age-and-gender && python3 setup.py install

# Begin SIP and PyQt build steps
# Update and install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-pyqt5.qtsvg \
    python3-pyqt5.qtwebkit \
    qt5-qmake \
    qtbase5-dev \
    qtbase5-dev-tools \
    libqt5svg5-dev \
    libqt5webenginewidgets5 \
    libqt5webchannel5-dev \
    qtwebengine5-dev \
    wget \
    expect \
    && rm -rf /var/lib/apt/lists/*

# Download and build SIP
RUN wget https://www.riverbankcomputing.com/static/Downloads/sip/4.19.25/sip-4.19.25.tar.gz \
    && tar -xvzf sip-4.19.25.tar.gz \
    && cd sip-4.19.25 \
    && python3 configure.py \
    && make \
    && make install \
    && cd ..

# Download and build PyQt
RUN wget https://files.pythonhosted.org/packages/8c/90/82c62bbbadcca98e8c6fa84f1a638de1ed1c89e85368241e9cc43fcbc320/PyQt5-5.15.0.tar.gz \
    && tar -xvzf PyQt5-5.15.0.tar.gz \
    && cd PyQt5-5.15.0 \
    && python3 configure.py --accept-license --verbose --qmake /usr/lib/aarch64-linux-gnu/qt5/bin/qmake
    && expect configure.exp \
    && make \
    && make install

# Command to run the Python script
# CMD ["python3", "./age-and-gender/example/example_live.py"]
