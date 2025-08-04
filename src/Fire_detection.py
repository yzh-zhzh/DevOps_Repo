from hal import hal_ir_sensor as ir_sensor
from hal import hal_temp_humidity_sensor as temp_humid_sensor
from hal import hal_adc as adc
import time
from threading import Thread
def initialise():
    ir_sensor.init()
    temp_humid_sensor.init()
    adc.init()

def smoke_detected():
    ir = ir_sensor.get_ir_sensor_state()
    ldr = adc.get_adc_value(0)  
    return ir and (ldr < 600)

def high_temp_detected():
    temp, _ = temp_humid_sensor.read_temp_humidity()
    if temp is not None:
        return temp > 40
    return False

def fire_detected():
    if smoke_detected():
        return True
    if high_temp_detected():
        return True
    return False