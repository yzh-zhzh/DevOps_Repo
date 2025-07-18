import time
from hal import hal_buzzer as buzzer
from hal import hal_servo as servo
from hal import hal_dc_motor as dc_motor
from lcd_display_controller import (
    set_override_mode,
    set_awaiting_password,
    update_lcd_line1,
    update_lcd_line2,
    lcd_lock
)
import queue

def keypad_manual_override_thread(system_state):
    shared_keypad_queue = system_state['shared_keypad_queue']
    password = ''
    awaiting_password = False

    while True:
        try:
            key = shared_keypad_queue.get_nowait()

            if key == '*':
                if system_state['fire_detected']:
                    awaiting_password = True
                    set_awaiting_password(True)
                    password = ''
                    with lcd_lock:
                        update_lcd_line2("Enter Password:")

            elif str(key).isdigit() and awaiting_password:
                password += key
                with lcd_lock:
                    update_lcd_line2(f"Entered: {password}")

                if len(password) >= 4:
                    if password == "1234":
                        system_state['fire_detected'] = False
                        system_state['system_override'] = True
                        buzzer.turn_off()
                        dc_motor.stop()
                        servo.set_servo_position(0)
                        set_override_mode(True)
                        with lcd_lock:
                            update_lcd_line1("Override Success")
                            update_lcd_line2("")
                    else:
                        with lcd_lock:
                            update_lcd_line1("Wrong Passcode")

                    password = ''
                    awaiting_password = False
                    set_awaiting_password(False)

        except queue.Empty:
            pass

        time.sleep(0.2)
