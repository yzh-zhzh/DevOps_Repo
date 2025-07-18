import time
from threading import Thread
import queue

from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_adc as adc
# from hal import hal_buzzer as buzzer
from hal import hal_keypad as keypad
from hal import hal_moisture_sensor as moisture_sensor
from hal import hal_servo as servo
from hal import hal_temp_humidity_sensor as temp_humid_sensor
from hal import hal_dc_motor as dc_motor

from lcd_display_controller import (
    lcd_display_thread,
    set_fire_detected,
    set_override_mode,
    set_awaiting_password
)
from fire_detection import fire_detection_thread
from keypad_manual_override import keypad_manual_override_thread
from water_adjustment import water_adjustment_thread
from sprinkler_confirmation import moisture_sensor_sprinkler_confirmation_thread
# from play_fire_tone import play_fire_alert_tone

# Shared resources
shared_keypad_queue = queue.Queue()

# Shared system state
system_state = {
    'fire_detected': False,
    'system_override': False,
    'shared_keypad_queue': shared_keypad_queue
}

def key_pressed(key):
    shared_keypad_queue.put(key)


def main():
    # Initialize all hardware components
    led.init()
    adc.init()
    # buzzer.init()
    moisture_sensor.init()
    dc_motor.init()
    servo.init()
    temp_humid_sensor.init()
    keypad.init(key_pressed)

    # Clear LCD once at startup (after LCD init)
    from lcd_display_controller import lcd, lcd_lock
    with lcd_lock:
        lcd.lcd_clear()

    # Wait briefly to ensure all hardware is initialized properly
    time.sleep(1)

    # Start all daemon threads
    Thread(target=keypad.get_key, daemon=True).start()
    Thread(target=fire_detection_thread, args=(system_state,), daemon=True).start()
    Thread(target=keypad_manual_override_thread, args=(system_state,), daemon=True).start()
    Thread(target=water_adjustment_thread, args=(system_state,), daemon=True).start()
    Thread(target=moisture_sensor_sprinkler_confirmation_thread, args=(system_state,), daemon=True).start()
    # Thread(target=play_fire_alert_tone, args=(system_state,), daemon=True).start()
    Thread(target=lcd_display_thread, daemon=True).start()

    # Keep main thread alive forever
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
