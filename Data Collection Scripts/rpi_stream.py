from flask import Flask, request
import io
import socket
import struct
from picamera import PiCamera
from threading import Thread

app = Flask(__name__)

# Flask server to receive the detected ID
@app.route('/receive_id', methods=['POST'])
def receive_id():
    data = request.json
    class_id = data['id']
    if class_id == 0:
        print("Turn Left")
    elif class_id == 1:
        print("Turn Right")
    return "OK"

# Function to stream video using Picamera
def stream_video():
    # Set up the camera
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 24

    # Set up the socket
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    # Accept a connection
    connection = server_socket.accept()[0].makefile('wb')

    try:
        # Stream video
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            stream.seek(0)
            stream.truncate()
    finally:
        connection.close()
        server_socket.close()

if __name__ == '__main__':
    # Start the Flask server in a separate thread
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=5001))
    flask_thread.start()

    # Start the video stream
    stream_video()