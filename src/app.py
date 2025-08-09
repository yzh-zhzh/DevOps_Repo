
from flask import Flask, jsonify, render_template, Response
import temp_humidity_sensor_data as temp_humidity
from picamera2 import Picamera2
from libcamera import Transform
import cv2
import numpy as np
import time

app = Flask(__name__)

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

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def dashboard():
    return render_template('Dashboard.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/camera')
def camera_page():
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def data():
    temperature, humidity = temp_humidity.read_data()
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "smoke": 25  # You can update this with real smoke data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
