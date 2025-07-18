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
    import lcd_display_controller
    password = ''

    while True:
        try:
            key = shared_keypad_queue.get_nowait()

            if key == '*':
                if system_state['fire_detected']:
                    password = ''
                    set_awaiting_password(True)
                    # The display thread will now show FIRE DETECTED! and Enter Passcode:

            elif str(key).isdigit() and lcd_display_controller.awaiting_password:
                password += key
                # The display thread will show Entered: ... if you want, but for now, just update state

                if len(password) >= 4:
                    if password == "1234":
                        system_state['fire_detected'] = False
                        system_state['system_override'] = True
                        buzzer.turn_off()
                        dc_motor.stop()
                        servo.set_servo_position(0)
                        set_override_mode(True)
                        set_awaiting_password(False)
                        # Show success message for 5 seconds directly
                        update_lcd_line1("Success!")
                        update_lcd_line2("Deactivated")
                        time.sleep(5)
                        # After 5 seconds, the display thread will show the default screen
                        password = ''
                    else:
                        # Show wrong passcode message for 5 seconds, then re-prompt
                        update_lcd_line2("Wrong Passcode!")
                        time.sleep(5)
                        password = ''
                        set_awaiting_password(True)

        except queue.Empty:
            pass

        time.sleep(0.2)
