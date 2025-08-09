from flask import Flask, jsonify, render_template
import mysql.connector
import temp_humidity_sensor_data as temp_humidity
 

app = Flask(__name__)

db_config = {
    'host': 'localhost',     # or your DB server IP
    'user': 'sensor_user',
    'password': 'YourStrongPassword',
    'database': 'sensor_data'
}

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

@app.route('/sensor-history')
def sensor_history():
    return render_template('sensor_history.html')


def insert_sensor_data(temp, humidity):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO temperature_log (temperature, humidity) VALUES (%s, %s)"
        cursor.execute(sql, (temp, humidity))
        conn.commit()
    except mysql.connector.Error as e:
        print("Error inserting data:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
@app.route('/sensor-history-data')
def sensor_history_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT recorded_at, temperature, humidity FROM temperature_log ORDER BY recorded_at ASC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        data = [
            {
                "timestamp": row[0].strftime("%Y-%m-%d %H:%M:%S"),
                "temperature": row[1],
                "humidity": row[2]
            }
            for row in rows
        ]
        return jsonify(data)
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data')
def data():
    # Read sensor data and return JSON
    temperature, humidity = temp_humidity.read_data()
    insert_sensor_data(temperature, humidity)
    data = {
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2)
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)