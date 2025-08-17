import time
from threading import Thread
from hal import hal_temp_humidity_sensor as temp_humid_sensor
from hal import hal_servo as servo
from hal import hal_dc_motor as dc_motor
from lcd_display_controller import set_fire_detected
from play_fire_tone import play_fire_alert_tone
import Fire_detection
from hal import hal_buzzer as buzzer
from lcd_display_controller import set_override_mode

def fire_detection_thread(system_state):
    buzzer_thread_started = False
    dc_motor.set_motor_speed(0) 
    while True:
        if Fire_detection.fire_detected():
            if not system_state['fire_detected']:
                system_state['fire_detected'] = True
                system_state['motor_locked'] = False   
                set_override_mode(False)               
                set_fire_detected(True)
                if not system_state.get('motor_locked', False):
                    dc_motor.set_motor_speed(100)
                servo.set_servo_position(100)
                if not buzzer_thread_started:
                    Thread(target=play_fire_alert_tone, args=(system_state,), daemon=True).start()
                    buzzer_thread_started = True
        else:
            if system_state['fire_detected']:
                system_state['fire_detected'] = False
                set_fire_detected(False)
        time.sleep(2)