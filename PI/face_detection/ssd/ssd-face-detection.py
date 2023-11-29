import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

# Load TFLite model and allocate tensors
interpreter = tflite.Interpreter(model_path="version-RFB-320_without_postprocessing.tflite")
interpreter.allocate_tensors()

# Get input and output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Start video capture
cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()
	if not ret:
		break

	# Resize and preprocess the frame for the model
	input_shape = input_details[0]['shape']
	input_data = cv2.resize(frame, (input_shape[1], input_shape[2]))
	input_data = np.expand_dims(input_data, axis=0)

	# Set the tensor values
	interpreter.set_tensor(input_details[0]['index'], input_data)

	# Invoke the interpreter
	interpreter.invoke()

	# Get the output details
	detections = interpreter.get_tensor(output_details[0]['index'])

	# Visualize or process the detections on the original frame
	for detection in detections[0]:
		# The values might be in the [ymin, xmin, ymax, xmax] format or similar.
		# Adapt the indices accordingly.
		ymin, xmin, ymax, xmax = detection[:4]
		cv2.rectangle(frame, (int(xmin * frame.shape[1]), int(ymin * frame.shape[0])),
			(int(xmax * frame.shape[1]), int(ymax * frame.shape[0])), (0, 255, 0), 2)

	cv2.imshow('Face Detection', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
