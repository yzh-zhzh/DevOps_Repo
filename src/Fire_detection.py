import time
from threading import Thread
import queue
from hal import hal_ir_sensor as ir_sensor
from hal import hal_temp_humidity_sensor as temp_humid_sensor
from hal import hal_adc as adc

def intialise():
    #initialization of HAL modules
    ir_sensor.init()
    temp_humid_sensor.init()
    adc.init()
    
def fire_detector(smoke_detected , high_temp):
    fire_detected = False
    if smoke_detected and high_temp == True:
        fire_detected == True
    else:
        fire_detected == False
    return fire_detected

def smoke_detector(IR_result, LDR_result):
    smoke_detector = False
    if IR_result == True and LDR_result == True: #Ensure both sensors detect smoke
        smoke_detector == True
    else:
        smoke_detector == False
    return smoke_detector


def IR_sensor(): #smoke detector
    IR_result = False
    ir_value = ir_sensor.get_ir_sensor_state()
    if ir_value == 1: # Smoke detected
        return IR_result == True
    else: 
        return IR_result == False
def LDR_sensor(): #smoke detector
    LDR_result = False
    LDR_value = adc.get_adc_value(0)
    if LDR_value < 100: # Smoke detected
        return LDR_result == True
    else:
        return LDR_result == False
def temp_sensor(): #Temperature sensor
    temperature = temp_sensor.read_temp_humidity()
    high_temp = False
    if temperature > 40: # High temperature detected
        return high_temp == True
    else:
        return high_temp == False