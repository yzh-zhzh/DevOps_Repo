from flask import Flask, jsonify, render_template, send_from_directory, Response
import json
import os
from datetime import datetime
import threading
import time
import sqlite3

# Try to import Raspberry Pi modules - fallback to mock if not available
try:
    from hal import hal_temp_humidity_sensor as temp_humidity
    from hal import hal_adc
    import RPi.GPIO as GPIO
    RPI_AVAILABLE = True
    print("Raspberry Pi HAL modules loaded successfully")
except ImportError as e:
    print(f"Raspberry Pi modules not available: {e}")
    print("Running in development mode with mock data")
    RPI_AVAILABLE = False

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuration
DATA_FILE = 'sensor_data.json'
DB_FILE = 'sensor_history.db'
UPDATE_INTERVAL = 3  # How often to read sensors and update data (seconds)

class SensorDataManager:
    def __init__(self, data_file, db_file):
        self.data_file = data_file
        self.db_file = db_file
        self.last_modified = 0
        self.cached_data = {
            'temperature': '--',
            'humidity': '--',
            'smoke': '--',
            'timestamp': datetime.now().isoformat()
        }
        self.lock = threading.Lock()
        self.init_database()
        self.init_sensors()
        
    def init_database(self):
        """Initialize SQLite database for sensor history"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    temperature REAL,
                    humidity REAL,
                    smoke REAL
                )
            ''')
            conn.commit()
            conn.close()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {e}")

    def init_sensors(self):
        """Initialize sensor hardware if available"""
        if RPI_AVAILABLE:
            try:
                temp_humidity.init()
                hal_adc.init()
                print("Sensors initialized successfully")
            except Exception as e:
                print(f"Error initializing sensors: {e}")
        
    def read_sensor_data(self):
        """Read data from physical sensors"""
        if not RPI_AVAILABLE:
            # Mock data for testing
            import random
            return {
                'temperature': round(20 + random.uniform(-5, 15), 1),
                'humidity': round(40 + random.uniform(-20, 40), 1),
                'smoke': round(random.uniform(0, 30), 1),
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            # Read temperature and humidity
            temp_humid_data = temp_humidity.read_temp_humidity()
            temperature = temp_humid_data[0] if temp_humid_data[0] > -50 else '--'
            humidity = temp_humid_data[1] if temp_humid_data[1] > -50 else '--'
            
            # Read smoke sensor (assuming it's connected to ADC channel 0)
            try:
                smoke_raw = hal_adc.get_adc_value(0)  # ADC channel 0
                # Convert ADC value (0-1023) to percentage (0-100)
                smoke = round((smoke_raw / 1023.0) * 100, 1)
            except:
                smoke = '--'
            
            return {
                'temperature': temperature,
                'humidity': humidity,
                'smoke': smoke,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error reading sensors: {e}")
            return {
                'temperature': '--',
                'humidity': '--',
                'smoke': '--',
                'timestamp': datetime.now().isoformat()
            }
    
    def save_data_to_file(self, data):
        """Save sensor data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data to file: {e}")
    
    def save_to_database(self, data):
        """Save sensor data to database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sensor_data (timestamp, temperature, humidity, smoke)
                VALUES (?, ?, ?, ?)
            ''', (
                data['timestamp'],
                data['temperature'] if data['temperature'] != '--' else None,
                data['humidity'] if data['humidity'] != '--' else None,
                data['smoke'] if data['smoke'] != '--' else None
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving to database: {e}")
    
    def update_sensor_data(self):
        """Read sensors and update cached data"""
        new_data = self.read_sensor_data()
        
        with self.lock:
            self.cached_data = new_data
            print(f"Sensor data updated: {new_data}")
        
        # Save to file and database
        self.save_data_to_file(new_data)
        self.save_to_database(new_data)
    
    def get_data(self):
        """Get current sensor data (thread-safe)"""
        with self.lock:
            return self.cached_data.copy()
    
    def get_history_data(self, limit=1000):
        """Get historical sensor data from database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, temperature, humidity, smoke
                FROM sensor_data
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            # Convert to list of dictionaries, newest first, then reverse for chronological order
            history = []
            for row in reversed(rows):  # Reverse to get chronological order
                history.append({
                    'timestamp': row[0],
                    'temperature': row[1] if row[1] is not None else 0,
                    'humidity': row[2] if row[2] is not None else 0,
                    'smoke': row[3] if row[3] is not None else 0
                })
            
            return history
            
        except Exception as e:
            print(f"Error fetching history data: {e}")
            return []

# Initialize sensor data manager
sensor_manager = SensorDataManager(DATA_FILE, DB_FILE)

def background_sensor_reader():
    """Background thread to continuously read sensors and update data"""
    while True:
        try:
            sensor_manager.update_sensor_data()
            time.sleep(UPDATE_INTERVAL)
        except Exception as e:
            print(f"Error in sensor reader: {e}")
            time.sleep(UPDATE_INTERVAL)

# Start background sensor reader
sensor_thread = threading.Thread(target=background_sensor_reader, daemon=True)
sensor_thread.start()

# Routes
@app.route('/')
def index():
    """Serve the login page"""
    return render_template('index.html')

@app.route('/data')
def get_sensor_data():
    """API endpoint to get current sensor data"""
    data = sensor_manager.get_data()
    return jsonify(data)

@app.route('/sensor-history-data')
def get_sensor_history():
    """API endpoint to get sensor history data"""
    history = sensor_manager.get_history_data()
    return jsonify(history)

@app.route('/dashboard.html')
@app.route('/dashboard')
def dashboard():
    """Serve the dashboard page"""
    return render_template('dashboard.html')

@app.route('/register.html')
@app.route('/register')
def register():
    """Serve the register page"""
    return render_template('register.html')

@app.route('/complete-profile.html')
@app.route('/complete-profile')
def complete_profile():
    """Serve the complete profile page"""
    return render_template('complete-profile.html')

@app.route('/profile.html')
@app.route('/profile')
def profile():
    """Serve the profile page"""
    return render_template('profile.html')

@app.route('/camera.html')
@app.route('/camera')
def camera():
    """Serve the camera page"""
    return render_template('camera.html')

@app.route('/sensor_log_history.html')
@app.route('/sensor_log_history')
def sensor_log_history():
    """Serve the sensor history page"""
    return render_template('sensor_log_history.html')

@app.route('/static/<path:filename>')
def serve_static_files(filename):
    """Serve static files (CSS, JS, images)"""
    return send_from_directory('static', filename)

# Test endpoint to manually update sensor data (for testing)
@app.route('/test-update')
def test_update():
    """Test endpoint to create sample data"""
    sensor_manager.update_sensor_data()
    return jsonify({'status': 'success', 'message': 'Sensor data updated'})

@app.route('/test-data')
def test_data():
    """Test endpoint to check if data is being generated"""
    data = sensor_manager.get_data()
    history_count = len(sensor_manager.get_history_data(10))
    return jsonify({
        'current_data': data,
        'history_records': history_count,
        'rpi_available': RPI_AVAILABLE
    })

if __name__ == '__main__':
    print(f"Starting Fire Alarm System server...")
    print(f"Raspberry Pi HAL available: {RPI_AVAILABLE}")
    print(f"Data file: {DATA_FILE}")
    print(f"Database file: {DB_FILE}")
    print(f"Sensor update interval: {UPDATE_INTERVAL} seconds")
    print(f"Access the application at: http://localhost:5000")
    
    # Create initial data file if it doesn't exist
    if not os.path.exists(DATA_FILE):
        initial_data = {
            'temperature': '--',
            'humidity': '--',
            'smoke': '--',
            'timestamp': datetime.now().isoformat()
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(initial_data, f, indent=2)
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)