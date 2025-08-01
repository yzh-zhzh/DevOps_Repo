import time
# from hal import hal_buzzer as buzzer
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
            print(f"[Keypad] Key pressed: {key}")

            if key == '*':
                print(f"[Keypad] Override requested. fire_detected={system_state['fire_detected']}")
                if system_state['fire_detected']:
                    password = ''
                    set_awaiting_password(True)
                    print(f"[Keypad] Awaiting passcode. awaiting_password={lcd_display_controller.awaiting_password}")

            elif str(key).isdigit() and lcd_display_controller.awaiting_password:
                if len(password) < 8:
                    password += str(key)
                lcd_display_controller.entered_passcode = password
                print(f"[Keypad] Passcode entered: {password}")

            elif key == '#' and lcd_display_controller.awaiting_password:
                print(f"[Keypad] Passcode confirm: {password}")
                if password == "1234":
                    print("[Keypad] Passcode correct. Shutting down system.")
                    system_state['fire_detected'] = False
                    system_state['system_override'] = True
                    system_state['motor_locked'] = True  # Prevent further DC motor control
                    # buzzer.turn_off()
                    dc_motor.set_motor_speed(0)  # Ensure DC motor stops
                    servo.set_servo_position(0)
                    set_override_mode(True)
                    set_awaiting_password(False)
                    lcd_display_controller.entered_passcode = ''
                    lcd_display_controller.override_success = True
                else:
                    print("[Keypad] Passcode incorrect.")
                    lcd_display_controller.passcode_error = True
                    time.sleep(2)
                    lcd_display_controller.passcode_error = False
                    lcd_display_controller.entered_passcode = password

        except queue.Empty:
            pass

        time.sleep(0.2)
