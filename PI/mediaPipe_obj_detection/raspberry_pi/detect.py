# Copyright 2023 The MediaPipe Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main scripts to run object detection."""

import argparse
import sys
import time
import threading

import cv2
import mediapipe as mp
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from .utils import visualize
from .sort import Sort

import paho.mqtt.client as mqtt
import requests

# Global variables to calculate FPS
COUNTER, FPS = 0, 0
START_TIME = time.time()
isStop = False
mqtt_topic_global = None
compress_rate = 0.4


def send_alive_check():
    global mqtt_topic_global
    while True:
        print("alive checking"+mqtt_topic_global)
        url = 'http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/report_alive/'
        data = {'sensorId': mqtt_topic_global}
        response = requests.post(url, data=data)
        print(response.text)
        time.sleep(10)  # Wait for 10 seconds before sending the next request.


def run(mqtt_topic: str, model: str = 'efficientdet.tflite', max_results: int = 5, score_threshold: float = 0.1, 
        camera_id: int = 0, width: int = 640, height: int = 360) -> None:
  """Continuously run inference on images acquired from the camera.

  Args:
    model: Name of the TFLite object detection model.
    max_results: Max of classification results.
    score_threshold: The score threshold of detection results.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
  """
  
  global mqtt_topic_global
  mqtt_topic_global = mqtt_topic
  
  # set the state to is_enable = true
  print("sending newest detection state")
  url = 'http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/sensor/update/'+mqtt_topic_global+'/'
  data = {'is_enable': 'true'}
  response = requests.post(url, data=data)
  print(response.text)

  # Start capturing video input from the camera
  cap = cv2.VideoCapture(camera_id)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  # Visualization parameters
  row_size = 50  # pixels
  left_margin = 24  # pixels
  text_color = (0, 0, 0)  # black
  font_size = 1
  font_thickness = 1
  fps_avg_frame_count = 10

  detection_frame = None
  detection_result_list = []
  
  # sort
  sort_tracker = Sort()
  
  # mqtt
  BROKER_ADDRESS = "1.tcp.au.ngrok.io"
  MQTT_TOPIC = mqtt_topic
  
  
  def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)
    
  def on_message(client, userdata, msg):
    print(f"{msg.topic} {str(msg.payload)}")
    message = msg.payload.decode("utf-8")
    print(message)
    global isStop
    if message == "STOP":
        print("detection stopped")
        isStop = True
        print("sending newest detection state")
        url = 'http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/sensor/update/'+mqtt_topic_global+'/'
        data = {'is_enable': 'false'}
        response = requests.post(url, data=data)
        print(response.text)
    elif message == "START":
        print("detection start")
        isStop = False
        print("sending newest detection state")
        url = 'http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/sensor/update/'+mqtt_topic_global+'/'
        data = {'is_enable': 'true'}
        response = requests.post(url, data=data)
        print(response.text)
    
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message
  
  client.connect(BROKER_ADDRESS, 26540, 60)
  
  client.loop_start()

  def save_result(result: vision.ObjectDetectorResult, unused_output_image: mp.Image, timestamp_ms: int):
      global FPS, COUNTER, START_TIME

      # Calculate the FPS
      if COUNTER % fps_avg_frame_count == 0:
          FPS = fps_avg_frame_count / (time.time() - START_TIME)
          START_TIME = time.time()
      
      # print(result.detections)
      detection_result_list.append(result)
      COUNTER += 1

  # Initialize the object detection model
  base_options = python.BaseOptions(model_asset_path=model)
  options = vision.ObjectDetectorOptions(base_options=base_options,
                                         running_mode=vision.RunningMode.LIVE_STREAM,
                                         max_results=max_results, score_threshold=score_threshold,
                                         result_callback=save_result)
  detector = vision.ObjectDetector.create_from_options(options)


  # Continuously capture images from the camera and run inference
  frequency = 1
  current_frame_count = 0
  
  
  # Start a new thread to send the alive check request every 30 seconds
  alive_check_thread = threading.Thread(target=send_alive_check)
  alive_check_thread.daemon = True  # This makes sure the thread will exit when the main program exits
  alive_check_thread.start()

  
  # the door exit tracking map that tracks the start and end location
  track_map = {}
  track_image_map = {}
  while cap.isOpened():
    if isStop is True:
      continue
    else: 
      #current_frame_count = (current_frame_count + 1) % frequency
      success, image = cap.read()
      if not success:
        sys.exit(
            'ERROR: Unable to read from webcam. Please verify your webcam settings.'
        )
      image = cv2.flip(image, 1)
      origin_image = image.copy()
      image = cv2.resize(image, (int(640*compress_rate), int(360*compress_rate)))

      # Convert the image from BGR to RGB as required by the TFLite model.
      rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

      # Run object detection using the model.
      if current_frame_count == 0:
          # print("run detection")
          detector.detect_async(mp_image, time.time_ns() // 1_000_000)
      # Show the FPS
      
      fps_text = 'FPS = {:.1f}'.format(FPS)
      # print(fps_text)
      text_location = (left_margin, row_size)
      current_frame = image
      cv2.putText(current_frame, fps_text, text_location, cv2.FONT_HERSHEY_DUPLEX,
                 font_size, text_color, font_thickness, cv2.LINE_AA)

      bboxes = []
      if detection_result_list:
          # print(detection_result_list)
          current_frame = visualize(current_frame, detection_result_list[0])
          for detection in detection_result_list[0].detections:
            bbox = detection.bounding_box
            x1, y1, x2, y2 = bbox.origin_x, bbox.origin_y, bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
            start_point = bbox.origin_x, bbox.origin_y
            end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
            category = detection.categories[0]
            category_name = category.category_name
            probability = round(category.score, 2)
            if category_name == 'person':
              # print([x1, y1, x2, y2, 1], category_name, probability)
              bboxes.append([x1, y1, x2, y2, 1])
          
          detection_frame = current_frame
          
          if bboxes:
            np_bboxes = np.array(bboxes)
          else:
            np_bboxes = np.empty((0,5))
          trackers = sort_tracker.update(np_bboxes)
            
          for tracking in trackers:
            x1, y1, x2, y2, track_id = map(int, tracking)
            if track_id in track_map:
              start_location = track_map[track_id][0]
              track_map[track_id] = (start_location, (x1, y1, x2, y2))
              start_image = track_image_map[track_id][0]
              track_image_map[track_id] = (start_image, origin_image)
              door_exit_detect(track_map[track_id][0], track_map[track_id][1], track_id, track_image_map[track_id], track_map, mqtt_topic)
            else:
              track_map[track_id] = ((x1, y1, x2, y2), (x1, y1, x2, y2))
              track_image_map[track_id] = (origin_image, origin_image)
              
            cv2.rectangle(detection_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(detection_frame, f'ID: {track_id}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
          detection_result_list.clear()

      if detection_frame is not None:
          cv2.imshow('object_detection', detection_frame)
      else:
          cv2.imshow('object_detection', current_frame)

      # Stop the program if the ESC key is pressed.
      if cv2.waitKey(1) == 27:
        break

  detector.close()
  cap.release()
  cv2.destroyAllWindows()
  
def door_exit_detect(startBBox, currentBBox, track_id, track_images, track_map, mqtt_topic):
  startX1, startY1, startX2, startY2 = startBBox
  currentX1, currentY1, currentX2, currentY2 = currentBBox
  startCenterX = startX1 + (startX2-startX1)/2
  currentCenterX = currentX1 + (currentX2-currentX1)/2
  print(f"start location: {startCenterX}, {startY1}, {track_id}")
  print(f"current location: {currentCenterX}, {currentY1}, {track_id}")
  
  height = int(360*compress_rate)
  width = int(640*compress_rate)
  
  if width*0.33 < startCenterX < width*0.66 and (currentCenterX < width*0.25 or currentCenterX > width*0.75):
    print(f"{track_id} exited the door!!!")
    # crop the image
    start_frame = track_images[0]
    end_frame = track_images[1]
    startY1 = 0 if startY1 < 0 else startY1
    startY2 = height if startY2 > height else startY2
    startX1 = 0 if startX1 < 0 else startX1
    startX2 = width if startX2 > width else startX2
    currentY1 = 0 if currentY1 < 0 else currentY1
    currentY2 = height if currentY2 > height else currentY2
    currentX1 = 0 if currentX1 < 0 else currentX1
    currentX2 = width if currentX2 > width else currentX2
    
    cropped_start_frame = start_frame[int(max(startY1-20, 0)//compress_rate):int(min(startY2+20, height)//compress_rate), int(max(startX1-20, 0)//compress_rate):int(min(startX2+20, width)//compress_rate)]
    cropped_end_frame = end_frame[int(max(currentY1-20, 0)//compress_rate):int(min(currentY2+20, height)//compress_rate), int(max(currentX1-20, 0)//compress_rate):int(min(currentX2+20, width)//compress_rate)]
    print(currentY1/compress_rate,currentY2//compress_rate, currentX1//compress_rate,currentX2//compress_rate)
    # save the image
    filename_start = "start-"+str(track_id)+".jpg"
    filename_end = "end-"+str(track_id)+".jpg"
    cv2.imwrite(filename_start, cropped_start_frame)
    cv2.imwrite(filename_end, cropped_end_frame)
    # send the notification
    url = 'http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/notification/create/'
    
    files = {'startPic': open(filename_start, 'rb'), 'endPic': open(filename_end, 'rb')}
    data = {'actionType':"LEAVEROOM", 'sensorId': mqtt_topic}
    response = requests.post(url, files=files, data=data)
    print(response.text)
    
    # delete the map pair
    del track_map[track_id]
    del track_images
    
  if (currentY2-currentY1 < (currentX2-currentX1)*0.5):
    print(f"{track_id} fall down!!!")
    # crop the image
    start_frame = track_images[0]
    end_frame = track_images[1]
    startY1 = 0 if startY1 < 0 else startY1
    startY2 = height if startY2 > height else startY2
    startX1 = 0 if startX1 < 0 else startX1
    startX2 = width if startX2 > width else startX2
    currentY1 = 0 if currentY1 < 0 else currentY1
    currentY2 = height if currentY2 > height else currentY2
    currentX1 = 0 if currentX1 < 0 else currentX1
    currentX2 = width if currentX2 > width else currentX2
    
    cropped_start_frame = start_frame[int(max(startY1-20, 0)//compress_rate):int(min(startY2+20, height)//compress_rate), int(max(startX1-20, 0)//compress_rate):int(min(startX2+20, width)//compress_rate)]
    cropped_end_frame = end_frame[int(max(currentY1-20, 0)//compress_rate):int(min(currentY2+20, height)//compress_rate), int(max(currentX1-20, 0)//compress_rate):int(min(currentX2+20, width)//compress_rate)]
    print(currentY1/compress_rate,currentY2//compress_rate, currentX1//compress_rate,currentX2//compress_rate)
    # save the image
    filename_start = "start-"+str(track_id)+".jpg"
    filename_end = "end-"+str(track_id)+".jpg"
    cv2.imwrite(filename_start, cropped_start_frame)
    cv2.imwrite(filename_end, cropped_end_frame)
    # send the notification
    url = 'http://watch-env.eba-9zamrd38.us-west-2.elasticbeanstalk.com/notification/create/'
    
    files = {'startPic': open(filename_start, 'rb'), 'endPic': open(filename_end, 'rb')}
    data = {'actionType':"FALLDOWN", 'sensorId': mqtt_topic}
    response = requests.post(url, files=files, data=data)
    print(response.text)
    
    # delete the map pair
    del track_map[track_id]
    del track_images
    
  

def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Path of the object detection model.',
      required=False,
      default='efficientdet.tflite')
  parser.add_argument(
      '--maxResults',
      help='Max number of detection results.',
      required=False,
      default=5)
  parser.add_argument(
      '--scoreThreshold',
      help='The score threshold of detection results.',
      required=False,
      type=float,
      default=0.25)
  # Finding the camera ID can be very reliant on platform-dependent methods. 
  # One common approach is to use the fact that camera IDs are usually indexed sequentially by the OS, starting from 0. 
  # Here, we use OpenCV and create a VideoCapture object for each potential ID with 'cap = cv2.VideoCapture(i)'.
  # If 'cap' is None or not 'cap.isOpened()', it indicates the camera ID is not available.
  parser.add_argument(
      '--cameraId', help='Id of camera.', required=False, type=int, default=0)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      type=int,
      default=640)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      type=int,
      default=360)
  args = parser.parse_args()

  run(args.model, int(args.maxResults),
      args.scoreThreshold, int(args.cameraId), args.frameWidth, args.frameHeight)


if __name__ == '__main__':
  main()
