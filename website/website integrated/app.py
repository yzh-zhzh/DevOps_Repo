
from flask import Flask, jsonify, render_template
import temp_humidity_sensor_data as temp_humidity
import time
from threading import Thread
#from camera import generate_frames

app = Flask(__name__)

# Global in-memory sensor history buffer
sensor_history = []

def sensor_data_collector():
    """Background thread to collect sensor data every 10 seconds"""
    while True:
        try:
            temperature, humidity = temp_humidity.read_data()
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            sensor_history.append({
                'timestamp': timestamp,
                'temperature': round(temperature, 2),
                'humidity': round(humidity, 2)
            })
            # Keep only last 100 records
            if len(sensor_history) > 100:
                sensor_history.pop(0)
        except Exception as e:
            print(f"Sensor read error: {e}")
        time.sleep(10)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/sensor_log_history')
def sensor_log_history_page():
    return render_template('sensor_log_history.html')

@app.route('/sensor-history-data')
def sensor_history_data():
    # Return sensor history as JSON
    return jsonify(sensor_history)

@app.route('/data')
def data():
    try:
        temperature, humidity = temp_humidity.read_data()
        return jsonify({
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "smoke": 25  # placeholder value
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/camera')
def camera_page():
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # Start the sensor data collection thread
    collector_thread = Thread(target=sensor_data_collector, daemon=True)
    collector_thread.start()
    app.run(host='0.0.0.0', port=5000)


