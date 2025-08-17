from hal import hal_input_switch
import time

def wait_for_switch_on():
    print("Waiting for slide switch to turn ON...")
    while True:
        if hal_input_switch.read_slide_switch():
            print("Slide switch is ON. Initializing system...")
            return
        time.sleep(0.2)
