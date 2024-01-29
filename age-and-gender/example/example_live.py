import cv2
import datetime
from age_and_gender import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json
import os

# Function to determine if a bounding box is close to the center of the frame
def is_close_to_center(box, frame_center, threshold=100):
    box_center = ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2)
    return abs(box_center[0] - frame_center[0]) <= threshold and abs(box_center[1] - frame_center[1]) 

# Initialize age and gender prediction
data = AgeAndGender()
data.load_shape_predictor('models/shape_predictor_5_face_landmarks.dat')
data.load_dnn_gender_classifier('models/dnn_gender_classifier_v1.dat')
data.load_dnn_age_predictor('models/dnn_age_predictor_v1.dat')

font = ImageFont.truetype("Acme-Regular.ttf", 20)
gst_pipeline = (
    "nvarguscamerasrc sensor-id=(int)0 ! "
    "video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)30/1 ! "
    "nvvidconv ! "
    "video/x-raw, width=(int)640, height=(int)480, format=(string)BGRx ! "
    "videoconvert ! "
    "appsink"
)
# Open a handle to the default webcam
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

# Get the size of the video frame
ret, frame = cap.read()
frame_height, frame_width, _ = (640, 480,3)
frame_center = (frame_width // 2, frame_height // 2)
start_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"results_{start_time}.json"
output_directory = 'results'
output_file_path = os.path.join(output_directory, filename)
os.makedirs(output_directory, exist_ok=True)


frames_directory = 'frames'
os.makedirs(frames_directory, exist_ok=True)

last_saved_time = datetime.datetime.now()
# Open a JSON file to write the results
with open(output_file_path, 'w') as outfile:
    outfile.write('[')  # Start a JSON array
    first_entry = True

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the captured frame to PIL Image
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame = cv2.resize(frame,(640,480))
        current_time = datetime.datetime.now()
#        if (current_time - last_saved_time).total_seconds() > 10:
#           frame_filename = os.path.join(frames_directory, f"frame_{current_time.strftime('%Y%m%d_%H%M%S')}.jpg")
#           cv2.imwrite(frame_filename, frame)
#           last_saved_time = current_time
        # Apply age and gender prediction
        result = data.predict(img)

        # Draw results on the frame and write to the file
        for info in result:
            if is_close_to_center(info['face'], frame_center):
                print("Face detected and close to the center")
                shape = [(info['face'][0], info['face'][1]), (info['face'][2], info['face'][3])]
                draw = ImageDraw.Draw(img)

                gender = info['gender']['value'].title()
                gender_percent = int(info['gender']['confidence'])
                age = info['age']['value']
                age_percent = int(info['age']['confidence'])

                # Save the results with timestamp and bounding box coordinates
                timestamp = datetime.datetime.now().isoformat()
                bbox = info['face']  # Bounding box coordinates
                entry = {
                    'timestamp': timestamp,
                    'age': age,
                    'gender': gender,
                    'bounding_box': {
                        'x1': bbox[0],
                        'y1': bbox[1],
                        'x2': bbox[2],
                        'y2': bbox[3]
                    }
                }

                # Write the entry to the JSON file
                if not first_entry:
                    outfile.write(',')
                json.dump(entry, outfile)
                first_entry = False
                outfile.flush()
                draw.text(
                    (info['face'][0] - 10, info['face'][3] + 10),
                    f"{gender} (~{gender_percent}%)\n{age} y.o. (~{age_percent}%)",
                    fill='white', font=font, align='center'
                )

                draw.rectangle(shape, outline="red", width=5)



    outfile.write(']')  # End the JSON array

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()

