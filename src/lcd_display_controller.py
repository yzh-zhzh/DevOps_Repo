import time
from threading import Lock
from hal import hal_lcd as LCD

# Shared variables to be updated externally
sprinkler_status_message = "Water OK"
water_volume_message = "Vol: 0%"
entered_override_mode = False
awaiting_password = False
fire_detected = False
lcd_lock = Lock()

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
    lcd = LCD.lcd()
    alternate = 0

    while True:
        with lcd_lock:
            if fire_detected and not entered_override_mode:
                lcd.lcd_display_string("FIRE DETECTED!", 1)
                if awaiting_password:
                    lcd.lcd_display_string("Enter Password:", 2)
                else:
                    if alternate == 0:
                        lcd.lcd_display_string("Volume: " + water_volume_message, 2)
                    elif alternate == 1:
                        lcd.lcd_display_string(sprinkler_status_message, 2)
                    elif alternate == 2:
                        lcd.lcd_display_string("* to override!", 2)
                    alternate = (alternate + 1) % 3
                time.sleep(5)
            else:
                lcd.lcd_display_string("Smart Fire Alert", 1)
                time.sleep(0.1)
                lcd.lcd_display_string("System Ready!", 2)
                time.sleep(0.1)

def update_lcd_line1(message):
    lcd = LCD.lcd()
    lcd.lcd_display_string(message.ljust(16), 1)

def update_lcd_line2(message):
    lcd = LCD.lcd()
    lcd.lcd_display_string(message.ljust(16), 2)