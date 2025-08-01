
import time
from hal import hal_adc as adc
from hal import hal_servo as servo
from hal import hal_dc_motor as dc_motor
from lcd_display_controller import update_water_volume

def water_adjustment_thread(system_state):
    sweep_pos = 0
    sweep_dir = 1
    while True:
        pot_val = adc.get_adc_value(1)
        pot_val = int((pot_val / 1023) * 100)
        # Only allow DC motor control if not locked by override
        if not system_state.get('motor_locked', False):
            dc_motor.set_motor_speed(pot_val)
            update_water_volume(f"Water Lvl: {pot_val}%")
        else:
            dc_motor.set_motor_speed(0)
            update_water_volume("Motor Locked!")

        # If fire detected and not overridden, servo sweeps back and forth
        if system_state['fire_detected'] and not system_state['system_override']:
            servo.set_servo_position(sweep_pos)
            sweep_pos += 10 * sweep_dir
            if sweep_pos >= 100:
                sweep_pos = 100
                sweep_dir = -1
            elif sweep_pos <= 0:
                sweep_pos = 0
                sweep_dir = 1
        time.sleep(0.1)

        
