import time
from hal import hal_buzzer as buzzer

def play_fire_alert_tone(system_state):
    while True:
        if system_state['fire_detected'] and not system_state.get('motor_locked', False):
            buzzer.turn_on()
            time.sleep(0.5)
            buzzer.turn_off()
            time.sleep(0.5)
        else:
            buzzer.turn_off()
            time.sleep(0.1)
