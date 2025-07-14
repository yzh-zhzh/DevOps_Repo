import time
from hal import hal_lcd as LCD
from hal import hal_moisture_sensor as moisture_sensor

def moisture_sensor_sprinkler_confirmation_thread(system_state):
    lcd = LCD.lcd()
    while True:
        if system_state['fire_detected'] and not system_state['system_override']:
            val = moisture_sensor.read_sensor()
            if val > 60:
                lcd.lcd_display_string("Water Released!", 1)
            else:
                lcd.lcd_display_string("Check Moisture Sensor!", 1)
        time.sleep(3)
