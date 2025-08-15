from flask import Flask, render_template, Response
from picamera2 import Picamera2, JpegEncoder
import io

app = Flask(__name__, template_folder='templates')

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

def generate_frames():
    stream = io.BytesIO()
    while True:
        stream.seek(0)
        picam2.capture_file(stream, format='jpeg')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + stream.getvalue() + b'\r\n')

@app.route('/camera')
def camera_page():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)

