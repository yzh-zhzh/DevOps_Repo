override_success = False
entered_passcode = ''
passcode_error = False


import time
from threading import Lock
from hal import hal_lcd as LCD
import os


sprinkler_status_message = "Water OK"
water_volume_message = "Vol: 0%"
entered_override_mode = False
awaiting_password = False
fire_detected = False
lcd_lock = Lock()


lcd = None
try:
    if os.path.exists('/dev/i2c-1'):
        lcd = LCD.lcd()
    else:
        print("/dev/i2c-1 not found. LCD will not be initialized.")
except Exception as e:
    print(f"LCD initialization failed: {e}")

def update_sprinkler_status(message):
    global sprinkler_status_message
    sprinkler_status_message = message[:16]

def update_water_volume(vol_str):
    global water_volume_message
    water_volume_message = vol_str[:16]

def set_override_mode(status=True):
    global entered_override_mode
    entered_override_mode = status

def set_awaiting_password(status=True):
    global awaiting_password
    awaiting_password = status

def set_fire_detected(status=True):
    global fire_detected
    fire_detected = status

def lcd_display_thread():
    global override_success, entered_override_mode, awaiting_password, fire_detected, passcode_error, entered_passcode, water_volume_message, sprinkler_status_message
    alternate = 0
    while True:
        with lcd_lock:
            if lcd is None:
                time.sleep(1)
                continue
            line1 = "Smart Fire Alert"
            line2 = "System Ready!"

            if override_success:
                line1 = "Override Success"
                line2 = "System Off!"
                lcd.lcd_display_string(line1.ljust(16), 1)
                lcd.lcd_display_string(line2.ljust(16), 2)
                time.sleep(3)
                override_success = False
                continue

            if fire_detected and not entered_override_mode:
                line1 = "FIRE DETECTED!"
                if awaiting_password:
                    if passcode_error:
                        line1 = "Wrong Passcode!"
                        line2 = "Try Again!"
                        lcd.lcd_display_string(line1.ljust(16), 1)
                        lcd.lcd_display_string(line2.ljust(16), 2)
                        time.sleep(2)
                        line1 = "Enter Passcode:"
                        line2 = entered_passcode
                        lcd.lcd_display_string(line1.ljust(16), 1)
                        lcd.lcd_display_string(line2.ljust(16), 2)
                        time.sleep(1)
                        continue
                    else:
                        line1 = "Enter Passcode:"
                        line2 = entered_passcode
                        lcd.lcd_display_string(line1.ljust(16), 1)
                        lcd.lcd_display_string(line2.ljust(16), 2)
                        time.sleep(1)
                        continue
                else:
                    if alternate == 0:
                        line2 = water_volume_message
                    elif alternate == 1:
                        line2 = sprinkler_status_message
                    elif alternate == 2:
                        line2 = "* to override!"
                    alternate = (alternate + 1) % 3
                    lcd.lcd_display_string(line1.ljust(16), 1)
                    lcd.lcd_display_string(line2.ljust(16), 2)
                    time.sleep(3)
                    continue
            else:
                lcd.lcd_display_string(line1.ljust(16), 1)
                lcd.lcd_display_string(line2.ljust(16), 2)
                time.sleep(1)

def update_lcd_line1(message):
    with lcd_lock:
        if lcd is not None:
            lcd.lcd_display_string(message.ljust(16), 1)

def update_lcd_line2(message):
    with lcd_lock:
        if lcd is not None:
            lcd.lcd_display_string(message.ljust(16), 2)