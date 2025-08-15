from flask import Flask, render_template, Response
from picamera2 import Picamera2
import io
import os
import time

app = Flask(__name__, template_folder='templates')

# Ensure folder structure exists
os.makedirs("templates", exist_ok=True)
os.makedirs("static/css", exist_ok=True)

# Start the camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

def generate_frames():
    stream = io.BytesIO()
    while True:
        try:
            stream.seek(0)
            picam2.capture_file(stream, format='jpeg')
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + stream.getvalue() + b'\r\n')
        except Exception as e:
            print(f"[Camera Error] {e}")
            time.sleep(0.1)  # small delay to avoid tight error loops

@app.route("/camera")
def camera_page():
    return render_template("camera.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    print("[Camera] CCTV server starting on http://0.0.0.0:5001/camera")
    app.run(host="0.0.0.0", port=5001, debug=False, threaded=True)


