import time
from hal import hal_servo as servo
from hal import hal_dc_motor as dc_motor
from lcd_display_controller import update_water_volume

def water_adjustment_thread(system_state):
    sweep_pos = 0
    sweep_dir = 1
    servo_reset = False
    while True:
        # DC motor control
        if system_state['fire_detected'] and not system_state.get('motor_locked', False):
            dc_motor.set_motor_speed(100)
            update_water_volume("Water Lvl: 100%")
        else:
            dc_motor.set_motor_speed(0)
            if system_state.get('motor_locked', False):
                update_water_volume("Motor Locked!")
            else:
                update_water_volume("Water Lvl: 0%")

        # Servo sweep logic
        if system_state['fire_detected'] and not system_state.get('motor_locked', False):
            servo.set_servo_position(sweep_pos)
            sweep_pos += 10 * sweep_dir
            if sweep_pos >= 180:
                sweep_pos = 180
                sweep_dir = -1
            elif sweep_pos <= 0:
                sweep_pos = 0
                sweep_dir = 1
            servo_reset = False
        else:
            if not servo_reset:
                servo.set_servo_position(0)
                sweep_pos = 0
                sweep_dir = 1
                servo_reset = True

        time.sleep(0.1)