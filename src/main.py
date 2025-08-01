import time
from threading import Thread
import queue
import RFID
import Fire_detection
from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_adc as adc
from hal import hal_buzzer as buzzer
from hal import hal_keypad as keypad
from hal import hal_moisture_sensor as moisture_sensor
from hal import hal_servo as servo
from hal import hal_temp_humidity_sensor as temp_humid_sensor
from hal import hal_dc_motor as dc_motor

from lcd_display_controller import lcd_display_thread

from Fire_detection import fire_detection_thread
from notify_alert import notify_fire_alert
from keypad_manual_override import keypad_manual_override_thread
from water_adjustment import water_adjustment_thread
from sprinkler_confirmation import moisture_sensor_sprinkler_confirmation_thread
from play_fire_tone import play_fire_alert_tone
from ultrasonic_data import ultrasonic_data_thread
# from camera_module import camera_thread
from play_fire_tone import play_fire_alert_tone

shared_keypad_queue = queue.Queue()

system_state = {
    'fire_detected': False,
    'system_override': False,
    'shared_keypad_queue': shared_keypad_queue
}

def key_pressed(key):
    shared_keypad_queue.put(key)

def initialize_hardware():
    led.init()
    adc.init()
    buzzer.init()
    moisture_sensor.init()
    dc_motor.init()
    servo.init()
    temp_humid_sensor.init()
    keypad.init(key_pressed)
    Fire_detection.initialise()
    # LCD clear
    from lcd_display_controller import lcd, lcd_lock
    with lcd_lock:
        lcd.lcd_clear()
    time.sleep(1)

def start_all_threads():
    Thread(target=keypad.get_key, daemon=True).start()
    Thread(target=fire_detection_thread, args=(system_state,), daemon=True).start()
    Thread(target=keypad_manual_override_thread, args=(system_state,), daemon=True).start()
    Thread(target=water_adjustment_thread, args=(system_state,), daemon=True).start()
    Thread(target=moisture_sensor_sprinkler_confirmation_thread, args=(system_state,), daemon=True).start()
    Thread(target=play_fire_alert_tone, args=(system_state,), daemon=True).start()
    Thread(target=lcd_display_thread, daemon=True).start()
    Thread(target=notify_fire_alert, args=(system_state,), daemon=True).start()
    Thread(target=ultrasonic_data_thread, args=(system_state,), daemon=True).start()
    # Thread(target=camera_thread, args=(system_state,), daemon=True).start()

def main():
    print("Waiting for RFID card to activate system...")
    while True:
        if RFID.RFID_reader():
            print("RFID detected! Activating all systems.")
            break
        time.sleep(1)

    initialize_hardware()
    start_all_threads()

    print("All sensors and systems are now running in the background.")

    # Main thread just keeps the program alive
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()