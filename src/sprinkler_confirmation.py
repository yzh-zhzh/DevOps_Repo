import time
from hal import hal_moisture_sensor as moisture_sensor
from lcd_display_controller import update_sprinkler_status

def moisture_sensor_sprinkler_confirmation_thread(system_state):
    moisture_sensor.init()
    while True:
        if system_state['fire_detected'] and not system_state['system_override']:
            val = moisture_sensor.read_sensor()
            print(f"[Moisture Sensor] Value: {val}")  # Debugging output
            if val > 0:  # Lower threshold for detection
                update_sprinkler_status("Water Released!")
            else:
                update_sprinkler_status("Check Sensor!")
        time.sleep(3)