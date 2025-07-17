import time
from hal import hal_lcd as LCD
from hal import hal_buzzer as buzzer
from hal import hal_servo as servo
from hal import hal_dc_motor as dc_motor
from lcd_display_controller import set_override_mode, set_awaiting_password
import queue

def keypad_manual_override_thread(system_state):
    shared_keypad_queue = system_state['shared_keypad_queue']
    lcd = LCD.lcd()
    password = ''
    awaiting_password = False

    while True:
        try:
            key = shared_keypad_queue.get_nowait()
            if key == '*':
                if system_state['fire_detected']:
                    awaiting_password = True
                    set_awaiting_password()
                    lcd.lcd_display_string("Enter Password:", 2)
                    password = ''
            elif key.isdigit() and awaiting_password:
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
                        lcd.lcd_display_string("", 2)
                        set_override_mode()
                    else:
                        lcd.lcd_display_string("Wrong Passcode", 1)
                    password = ''
                    awaiting_password = False
        except queue.Empty:
            pass

        time.sleep(0.2)
