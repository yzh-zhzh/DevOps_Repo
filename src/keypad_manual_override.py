import time
import queue
from hal import hal_lcd as LCD
from hal import hal_buzzer as buzzer
from hal import hal_dc_motor as dc_motor
from hal import hal_servo as servo

def keypad_manual_override_thread(system_state):
    lcd = LCD.lcd()
    password = ''
    q = system_state['shared_keypad_queue']
    while True:
        try:
            key = q.get_nowait()
            if key == '*':
                password = ''
                lcd.lcd_display_string("Override Cancelled", 2)
            elif key.isdigit():
                password += key
                lcd.lcd_display_string(f"Entered: {password}", 2)
                if len(password) >= 4:
                    if password == "0735":
                        system_state['fire_detected'] = False
                        system_state['system_override'] = True
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
