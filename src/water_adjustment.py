import time
from hal import hal_adc as adc
from hal import hal_servo as servo
from lcd_display_controller import update_water_volume

def water_adjustment_thread(system_state):
    while True:
        pot_val = adc.get_adc_value(1)
        pot_val = int((pot_val / 1023) * 100)
        if system_state['fire_detected'] and not system_state['system_override']:
            servo.set_servo_position(pot_val)
            update_water_volume(f"Water Lvl: {pot_val}%")
        # Prevent DC motor from restarting if override is active
        if system_state['system_override']:
            dc_motor.set_motor_speed(0)
        time.sleep(1)

        
