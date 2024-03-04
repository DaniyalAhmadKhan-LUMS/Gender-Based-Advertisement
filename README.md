# Gender Detection on Jetson Nano

## Project Description
This repository hosts a robust solution for real-time gender detection utilizing a Jetson Nano. The core of this application uses `dlib` for facial feature extraction to classify a person's gender and age. This project is particularly designed to run efficiently on a Jetson Nano, leveraging the power of a CSI camera for video input. After detecting the age and gender, the application plays specific videos from a folder based on the detected gender or a generic video in the absence of detection. This end-to-end process involves compiling OpenCV with GStreamer and CUDA for performance optimization and developing a custom PyQt video player for the output display.

## Installation

### Prerequisites
- Python 3.9
- cmake
- PyQt5
- A Linux-based OS (preferably Ubuntu for Jetson Nano)

### Setup Environment
1. Navigate to your projects directory:
    ```bash
    cd ~/Documents
    ```
2. Clone the repository:
    ```bash
    git clone https://github.com/DaniyalAhmadKhan-LUMS/age-gender.git
    ```
3. Create a Python virtual environment and activate it:
    ```bash
    mkdir envs && cd envs
    sudo apt update && sudo apt install python3.8-venv
    python3 -m venv ageGen --system-site-packages
    source ageGen/bin/activate
    ```
4. Install system dependencies:
    ```bash
    sudo apt-get update && sudo apt-get install -y cmake nano libgl1-mesa-glx build-essential python3-dev python3-pip python3-pyqt5.qtsvg python3-pyqt5.qtwebkit
    ```

### Compile PyQt from Source
Ensure you are in the Documents folder or navigate back using `cd ~/Documents`.
1. Download and install SIP:
    ```bash
    wget https://www.riverbankcomputing.com/static/Downloads/sip/4.19.25/sip-4.19.25.tar.gz
    tar -xvzf sip-4.19.25.tar.gz && cd sip-4.19.25
    python3 configure.py && make && make install
    cd ..
    ```
2. Download and install PyQt:
    ```bash
    wget https://files.pythonhosted.org/packages/8c/90/82c62bbbadcca98e8c6fa84f1a638de1ed1c89e85368241e9cc43fcbc320/PyQt5-5.15.0.tar.gz
    tar -xvzf PyQt5-5.15.0.tar.gz && cd PyQt5-5.15.0
    sudo apt-get install -y qt5-qmake qtbase5-dev qtbase5-dev-tools libqt5svg5-dev libqt5webenginewidgets5 libqt5webchannel5-dev qtwebengine5-dev
    echo yes | python3 configure.py --confirm-license --verbose --qmake /usr/lib/aarch64-linux-gnu/qt5/bin/qmake
    sudo apt install python3-pyqt5.qtmultimedia -y
    ```

### Install Project Dependencies
Navigate to the `age-gender/age-and-gender` directory:
```bash
cd ~/Documents/age-gender/age-and-gender
```
Install required Python packages:
```bash
pip install wheel numpy face_recognition opencv-python-headless
```
```bash
python setup.py install
```
## Usage
### Running the Inference Script:
To run the gender detection, ensure you're in the correct directory and the `ageGen` environment is activated:
```bash
cd age-gender/age-and-gender/example
```
```bash
python example_live.py
```
### Running the Video Player
Open a separate terminal, activate the `ageGen` environment again, and navigate to the video player directory:
```bash
cd ~/Documents/age-gender/age-and-gender/video_player
```
```bash
source ../../envs/ageGen/bin/activate
```
```bash
python player.py
```
## Additional Notes
* The project is set up to compile `OpenCV` with `GStreamer` and `CUDA` enabled, enhancing performance on the Jetson Nano.
* The custom PyQt video player requires PyQt to be compiled from the source, following the provided installation instructions.
* This setup is intended for users with a basic understanding of Linux-based systems and command-line interfaces.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
