import time
from hal import hal_buzzer as buzzer

def play_fire_alert_tone(system_state):
    while system_state['fire_detected'] and not system_state['system_override']:
        buzzer.turn_on()
        time.sleep(0.5)
        buzzer.turn_off()
        time.sleep(0.5)
