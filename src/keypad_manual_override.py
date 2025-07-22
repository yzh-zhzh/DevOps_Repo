import time
from hal import hal_buzzer as buzzer
from hal import hal_servo as servo
from hal import hal_dc_motor as dc_motor
from lcd_display_controller import (
    set_override_mode,
    set_awaiting_password,
    update_lcd_line1,
    update_lcd_line2,
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
                    update_lcd_line1("Enter Passcode:")
                    update_lcd_line2("")

            elif str(key).isdigit() and lcd_display_controller.awaiting_password:
                if len(password) < 8:  # Limit passcode length for display
                    password += key
                update_lcd_line2(password)

            elif key == '#' and lcd_display_controller.awaiting_password:
                if password == "1234":
                    system_state['fire_detected'] = False
                    system_state['system_override'] = True
                    buzzer.turn_off()
                    dc_motor.stop()
                    servo.set_servo_position(0)
                    set_override_mode(True)
                    set_awaiting_password(False)
                    # Show system ready message
                    update_lcd_line1("Smart Fire System")
                    update_lcd_line2("System Ready!")
                    password = ''
                else:
                    # Show wrong passcode message for 2 seconds, then re-prompt
                    update_lcd_line1("Wrong Passcode!")
                    update_lcd_line2("Pls Try Again!")
                    time.sleep(2)
                    update_lcd_line1("Enter Passcode:")
                    update_lcd_line2(password)

        except queue.Empty:
            pass

        time.sleep(0.2)
