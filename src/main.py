import time
from threading import Thread
import queue

from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_adc as adc
from hal import hal_buzzer as buzzer
from hal import hal_keypad as keypad
from hal import hal_moisture_sensor as moisture_sensor
from hal import hal_servo as servo
from hal import hal_temp_humidity_sensor as temp_humid_sensor
from hal import hal_dc_motor as dc_motor

# Shared resources
shared_keypad_queue = queue.Queue()
system_override = False
fire_detected = False

def key_pressed(key):
    shared_keypad_queue.put(key)

def fire_detection_thread():
    global fire_detected
    lcd = LCD.lcd()
    buzzer_thread_started = False  # Track if buzzer tone thread is already running

    while True:
        temp, humid = temp_humid_sensor.read_temp_humidity()
        if temp > 50:  # Assume fire condition
            if not fire_detected:
                fire_detected = True
                lcd.lcd_clear()
                lcd.lcd_display_string("FIRE DETECTED!", 1)
                dc_motor.set_motor_speed(100)
                servo.set_servo_position(100)  # Full water release
                if not buzzer_thread_started:
                    Thread(target=play_fire_alert_tone, daemon=True).start()
                    buzzer_thread_started = True
        time.sleep(2)


def keypad_manual_override_thread():
    global system_override, fire_detected
    lcd = LCD.lcd()
    password = ''
    while True:
        try:
            key = shared_keypad_queue.get_nowait()
            if key == '*':
                password = ''
                lcd.lcd_display_string("Override Cancelled", 2)
            elif key.isdigit():
                password += key
                lcd.lcd_display_string(f"Entered: {password}", 2)
                if len(password) >= 4:
                    if password == "0735":
                        fire_detected = False
                        system_override = True
                        buzzer.turn_off()
                        dc_motor.stop()
                        servo.set_servo_position(0)
                        lcd.lcd_display_string("Override Success", 1)
                    else:
                        lcd.lcd_display_string("Wrong Passcode", 1)
                    password = ''
        except queue.Empty:
            pass
        time.sleep(0.2)

def water_adjustment_thread():
    lcd = LCD.lcd()
    while True:
        pot_val = adc.get_adc_value(1)
        pot_val = int((pot_val / 1023) * 100)
        if fire_detected and not system_override:
            servo.set_servo_position(pot_val)
            lcd.lcd_display_string(f"Water Level: {pot_val}%", 2)
        time.sleep(1)

def moisture_sensor_sprinkler_confirmation_thread():
    lcd = LCD.lcd()
    while True:
        if fire_detected and not system_override:
            sensor_val = moisture_sensor.read_sensor()
            if sensor_val > 60:
                lcd.lcd_display_string("Water Released!", 1)
            else:
                lcd.lcd_display_string("Check Moisture Sensor!", 1)
        time.sleep(3)

def play_fire_alert_tone():
    while fire_detected and not system_override:
        buzzer.turn_on()
        time.sleep(0.5)
        buzzer.turn_off()
        time.sleep(0.5)

def main():
    # Init all hardware
    led.init()
    adc.init()
    buzzer.init()
    moisture_sensor.init()
    dc_motor.init()
    servo.init()
    temp_humid_sensor.init()
    keypad.init(key_pressed)

    lcd = LCD.lcd()
    lcd.lcd_clear()
    lcd.lcd_display_string("Smart Fire Alert", 1)

    # Threads
    Thread(target=keypad.get_key, daemon=True).start()
    Thread(target=fire_detection_thread, daemon=True).start()
    Thread(target=keypad_manual_override_thread, daemon=True).start()
    Thread(target=water_adjustment_thread, daemon=True).start()
    Thread(target=moisture_sensor_sprinkler_confirmation_thread, daemon=True).start()
    Thread(target=play_fire_alert_tone, daemon=True).start()

    # Keep main thread alive
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()