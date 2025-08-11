from flask import Flask, jsonify, render_template, send_from_directory
import json
import os
from datetime import datetime
import threading
import time

app = Flask(__name__, static_folder='website/website integrated', template_folder='website/website integrated')

# Configuration
DATA_FILE = 'sensor_data.json'  # Path to your JSON file
UPDATE_INTERVAL = 1  # How often to check for file updates (seconds)

class SensorDataManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.last_modified = 0
        self.cached_data = {
            'temperature': '--',
            'humidity': '--',
            'smoke': '--',
            'timestamp': datetime.now().isoformat()
        }
        self.lock = threading.Lock()
        
    def get_file_modified_time(self):
        """Get the last modified time of the JSON file"""
        try:
            return os.path.getmtime(self.data_file)
        except OSError:
            return 0
    
    def load_data_from_file(self):
        """Load sensor data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return {
                    'temperature': data.get('temperature', '--'),
                    'humidity': data.get('humidity', '--'),
                    'smoke': data.get('smoke', '--'),
                    'timestamp': data.get('timestamp', datetime.now().isoformat())
                }
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error reading sensor data: {e}")
            return {
                'temperature': '--',
                'humidity': '--',
                'smoke': '--',
                'timestamp': datetime.now().isoformat()
            }
    
    def update_cache_if_needed(self):
        """Update cached data if file has been modified"""
        current_modified = self.get_file_modified_time()
        
        if current_modified > self.last_modified:
            with self.lock:
                new_data = self.load_data_from_file()
                self.cached_data = new_data
                self.last_modified = current_modified
                print(f"Data updated: {new_data}")
    
    def get_data(self):
        """Get current sensor data (thread-safe)"""
        self.update_cache_if_needed()
        with self.lock:
            return self.cached_data.copy()

# Initialize sensor data manager
sensor_manager = SensorDataManager(DATA_FILE)

def background_file_watcher():
    """Background thread to continuously monitor file changes"""
    while True:
        try:
            sensor_manager.update_cache_if_needed()
            time.sleep(UPDATE_INTERVAL)
        except Exception as e:
            print(f"Error in file watcher: {e}")
            time.sleep(UPDATE_INTERVAL)

# Start background file watcher
watcher_thread = threading.Thread(target=background_file_watcher, daemon=True)
watcher_thread.start()

# Routes
@app.route('/')
def index():
    """Serve the login page"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/data')
def get_sensor_data():
    """API endpoint to get current sensor data"""
    data = sensor_manager.get_data()
    return jsonify(data)

@app.route('/dashboard.html')
def dashboard():
    """Serve the dashboard page"""
    return send_from_directory(app.static_folder, 'dashboard.html')

@app.route('/register.html')
def register():
    """Serve the register page"""
    return send_from_directory(app.static_folder, 'register.html')

@app.route('/complete-profile.html')
def complete_profile():
    """Serve the complete profile page"""
    return send_from_directory(app.static_folder, 'complete-profile.html')

@app.route('/profile.html')
def profile():
    """Serve the profile page"""
    return send_from_directory(app.static_folder, 'profile.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    """Serve static files (CSS, JS, images)"""
    return send_from_directory(app.static_folder, filename)

# Test endpoint to manually update sensor data (for testing)
@app.route('/test-update')
def test_update():
    """Test endpoint to create sample data"""
    test_data = {
        'temperature': 25.5,
        'humidity': 60.2,
        'smoke': 15.0,
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(test_data, f, indent=2)
        return jsonify({'status': 'success', 'message': 'Test data created'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    # Create sample data file if it doesn't exist
    if not os.path.exists(DATA_FILE):
        initial_data = {
            'temperature': '--',
            'humidity': '--',
            'smoke': '--',
            'timestamp': datetime.now().isoformat()
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(initial_data, f, indent=2)
    
    print(f"Starting Fire Alarm System server...")
    print(f"Monitoring data file: {DATA_FILE}")
    print(f"Access the application at: http://localhost:5000")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)


