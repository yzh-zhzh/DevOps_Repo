from picamera2 import Picamera2
from libcamera import Transform
import cv2
import numpy as np
import time

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}, transform=Transform(hflip=1)))
picam2.start()

def generate_frames():
    while True:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.1)  # Adjust frame rate as needed