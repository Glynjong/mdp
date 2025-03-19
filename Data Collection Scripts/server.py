import cv2
import numpy as np
import socket
import struct
import requests
import io
from ultralytics import YOLO  # Import YOLO from Ultralytics

# Load the YOLO model
model = YOLO('task2_jet.pt')  # Replace with your model path

# Define the mapping from class names to IDs
class_mapping = {
    "left": 0,
    "right": 1
}

# Function to send the detected ID to the RPI
def send_id_to_rpi(class_id):
    url = 'http://192.168.19.1:5001/receive_id'  # Replace <RPI_IP> with the RPI's IP address
    data = {'id':class_id}
    try:
        response = requests.post(url, json=data)
        print(f"Sent ID {class_id} to RPI. Response: {response.status_code}")
    except Exception as e:
        print(f"Failed to send ID to RPI: {e}")

# Function to perform detection
def detect_objects(frame):
    # Perform inference
    results = model(frame)

    # Process detections
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # Bounding box coordinates
        confidences = result.boxes.conf.cpu().numpy()  # Confidence scores
        class_ids = result.boxes.cls.cpu().numpy()  # Class IDs

        for box, conf, cls in zip(boxes, confidences, class_ids):
            if conf > 0.5:  # Confidence threshold
                x1, y1, x2, y2 = box
                class_name = list(class_mapping.keys())[int(cls)]
                class_id = class_mapping[class_name]
                print(f"Detected: {class_name} (ID: {class_id})")

                # Send the detected ID to the RPI
                send_id_to_rpi(class_id)

                # Draw bounding box
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, class_name, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame  # Only return the processed frame

# Set up the socket to receive the video stream
client_socket = socket.socket()
client_socket.connect(('192.168.19.1', 8000))  # Replace <RPI_IP> with the RPI's IP address
connection = client_socket.makefile('rb')

try:
    while True:
        # Read the length of the image
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break

        # Read the image data
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)
        image = cv2.imdecode(np.frombuffer(image_stream.read(), dtype=np.uint8), cv2.IMREAD_COLOR)

        # Perform object detection
        processed_frame = detect_objects(image)  # Only unpack one value

        # Display the frame with bounding boxes
        cv2.imshow('Live Feed with Detections', processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    connection.close()
    client_socket.close()
    cv2.destroyAllWindows()