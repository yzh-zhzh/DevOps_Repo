from flask import Flask, jsonify, Response
import time
import numpy as np

app = Flask(__name__)

@app.route('/')
def root():
    return 'Smart Fire Alert System (Simulator) is running. Endpoints: /data, /video_feed'

@app.route('/data')
def data():
    # Simulated sensor readings
    # Replace with real values from your sensors on the Raspberry Pi build
    temperature = 26.5 + np.random.randn() * 0.2
    humidity = 60.0 + np.random.randn() * 0.5
    smoke = max(0, int(20 + np.random.randn() * 5))
    return jsonify({
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "smoke": smoke
    })

def generate_frames():
    # Generate a static PNG image as a placeholder MJPEG stream (no cv2)
    from io import BytesIO
    import matplotlib.pyplot as plt
    w, h = 640, 360
    # Create a simple gradient image
    x = np.linspace(0, 1, w)
    y = np.linspace(0, 1, h)
    xv, yv = np.meshgrid(x, y)
    frame = np.clip(0.5 + 0.5 * np.sin(2 * np.pi * (xv + yv)), 0, 1)
    # Use matplotlib to save as PNG in memory
    fig, ax = plt.subplots(figsize=(w/100, h/100), dpi=100)
    ax.axis('off')
    ax.imshow(frame, cmap='gray', vmin=0, vmax=1)
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    img_bytes = buf.getvalue()
    buf.close()
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + img_bytes + b'\r\n')
        time.sleep(0.2)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)