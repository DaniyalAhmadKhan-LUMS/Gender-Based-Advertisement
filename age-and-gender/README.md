
# Gender Detection on Jetson Nano

The code in this repo uses dlib to extract the facial features of a person and detect thier gender.
## Requirements: Python3.9, cmake

To setup the repo on a linux machine clone the repo using `git clone https://github.com/DaniyalAhmadKhan-LUMS/age-gender.git` and run the following commands:
1) `apt-get update && apt-get install -y cmake nano libgl1-mesa-glx`
2) `pip install numpy face_recognition opencv-python-headless`
3) `cd age-and-gender && python setup.py install`

To run the live demo navigate to age-and-gender directory and run:
`python example_live.py`

