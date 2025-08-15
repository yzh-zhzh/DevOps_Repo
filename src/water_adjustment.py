import time
import threading
import RPi.GPIO as GPIO
from hal import hal_servo as servo
from hal import hal_dc_motor as dc_motor
from hal import hal_adc as adc
from lcd_display_controller import update_water_volume

servo_lock = threading.Lock()

def water_adjustment_thread(system_state):
    sweep_pos = 0
    sweep_dir = 1
    sweep_pos = 0
    sweep_dir = 1
    servo_reset = False
    last_servo_pos = None
    while True:
        if system_state['fire_detected'] and not system_state.get('motor_locked', False):
            pot_val = adc.get_adc_value(1)
            speed = int((pot_val / 1023) * 100)
            dc_motor.set_motor_speed(speed)
            update_water_volume(f"Water Lvl: {speed}%")
            with servo_lock:
                if last_servo_pos != sweep_pos:
                    servo.set_servo_position(sweep_pos)
                    last_servo_pos = sweep_pos
            sweep_pos += 10 * sweep_dir
            if sweep_pos >= 180:
                sweep_pos = 180
                sweep_dir = -1
            elif sweep_pos <= 0:
                sweep_pos = 0
                sweep_dir = 1
            servo_reset = False
        else:
            dc_motor.set_motor_speed(0)
            if system_state.get('motor_locked', False):
                update_water_volume("Motor Locked!")
            else:
                update_water_volume("Water Lvl: 0%")
            if not servo_reset:
                with servo_lock:
                    if last_servo_pos != 0:
                        servo.set_servo_position(0)
                        last_servo_pos = 0
                sweep_pos = 0
                sweep_dir = 1
                servo_reset = True
        time.sleep(0.1)