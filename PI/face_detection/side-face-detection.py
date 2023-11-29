import cv2
import numpy as np
import time
import requests
import os

# ------------------------------------------------------------------------------
# automaticdai
# YF Robotics Labrotary
# Instagram: yfrobotics
# Twitter: @yfrobotics
# Website: https://www.yfrl.org
# ------------------------------------------------------------------------------
# Reference:
# - https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81
# ------------------------------------------------------------------------------

fps = 0
# Define the codec using VideoWriter_fourcc and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None
is_recording = False
video_filename = "output.avi"

face_counter = 0
no_face_counter = 0
frame_counter = 0 
MAX_FRAMES = 1800  # Assuming 30 FPS * 60 seconds = 1800 frames for 1 minute

detect_frame_counter = 0
DETECTION_FREQUENCY = 6


def visualize_fps(image, fps: int):
    if len(np.shape(image)) < 3:
        text_color = (255, 255, 255)  # white
    else:
        text_color = (0, 255, 0)  # green
    row_size = 20  # pixels
    left_margin = 24  # pixels

    font_size = 1
    font_thickness = 1

    # Draw the FPS counter
    fps_text = 'FPS = {:.1f}'.format(fps)
    text_location = (left_margin, row_size)
    cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                font_size, text_color, font_thickness)

    return image


# Load the cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)
# To use a video file as input
# cap = cv2.VideoCapture('filename.mp4')

while True:
    # ----------------------------------------------------------------------
    # record start time
    start_time = time.time()
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    if is_recording:
        out.write(img)
    
    if detect_frame_counter % DETECTION_FREQUENCY == 0:
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) > 0:
            print("Found {} faces!".format(len(faces)))
            face_counter += 1
            no_face_counter = 0  # Reset no face counter
        else:
            print("No faces found!")
            no_face_counter += 1
            face_counter = 0  # Reset face counter
        
        # If three consecutive frames with a face are detected and we are not currently recording
        if face_counter == 3 and not is_recording:
            out = cv2.VideoWriter(video_filename, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
            is_recording = True
            print("Recording started!")

        # If a face is detected and we are recording
        if len(faces) > 0 and is_recording:
            # out.write(img)
            frame_counter += 1

    # If three consecutive frames without a face are detected or the frame_counter reaches maximum, 
    # and we are recording
    if (no_face_counter == 3 or frame_counter >= MAX_FRAMES) and is_recording:
        out.release()
        is_recording = False
        print("Recording stopped!")
        
        # POST the video to your server
        with open(video_filename, 'rb') as f:
            # response = requests.post('http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/upload_video/', data={'title': "output.avi"}, files={'video_file': ("output.avi",f)})
            print("Video sent to server!")
            # print(response.text)
            break
        


        # Optional: delete the video file after sending
        # os.remove(video_filename)
        frame_counter = 0  # Reset frame counter
    


    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # Display
    cv2.imshow('img', visualize_fps(img, fps))
    # ----------------------------------------------------------------------
    # record end time
    end_time = time.time()
    # calculate FPS
    seconds = end_time - start_time
    fps = 1.0 / seconds
    print("Estimated fps:{0:0.1f}".format(fps))

    # Always increment the detect_frame_counter
    detect_frame_counter += 1

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

# Release the VideoCapture object
cap.release()
