from flask import Flask, jsonify, render_template
import temp_humidity_sensor_data as temp_humidity

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    # Allow any domain to access the API
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def dashboard():
    # Serve the dashboard HTML page
    return render_template('Dashboard.html')

@app.route('/profile')
def profile():
    # Serve the profile HTML page
    return render_template('profile.html')


@app.route('/data')
def data():
    # Read sensor data and return JSON
    temperature, humidity = temp_humidity.read_data()
    data = {
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2)
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)