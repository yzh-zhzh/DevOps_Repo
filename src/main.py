import time
from threading import Thread
import queue


from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_adc as adc
from hal import hal_buzzer as buzzer
from hal import hal_keypad as keypad
from hal import hal_moisture_sensor as moisture_sensor
from hal import hal_input_switch as input_switch
from hal import hal_ir_sensor as ir_sensor
from hal import hal_rfid_reader as rfid_reader
from hal import hal_servo as servo
from hal import hal_temp_humidity_sensor as temp_humid_sensor
from hal import hal_usonic as usonic
from hal import hal_dc_motor as dc_motor
from hal import hal_accelerometer as accel

#Empty list to store sequence of keypad presses
shared_keypad_queue = queue.Queue()

   


#Call back function invoked when any key on keypad is pressed
def key_pressed(key):
    shared_keypad_queue.put(key)


def main():
    #initialization of HAL modules
    led.init()
    adc.init()
    buzzer.init()
  
    moisture_sensor.init()
    input_switch.init()
    ir_sensor.init()
    reader = rfid_reader.init()
    servo.init()
    temp_humid_sensor.init()
    usonic.init()
    dc_motor.init()
    accelerometer = accel.init()

    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    lcd = LCD.lcd()
    lcd.lcd_clear()
    while (True):
        IR_sensor()
        LDR_sensor()
        RFID_reader()
        Ultrasonic_sensor()
        temp_sensor()
        moisture_sensor()
        humidity_sensor()
        smoke_detector()
        fire_detector()
    
#  FIRE DETECTION LOGIC
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

#  SENSOR LOGIC
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
    
def RFID_reader(): #Start button
    Start_button = False
    id = rfid_reader.read_id_no_block()
    if id != "None": # RFID card detected
        return Start_button == True
    else:
        return Start_button == False
def Ultrasonic_sensor(): #Person detection
    Person_detected = False
    distance = usonic.get_distance()
    if distance < 20: # Person detected
        return Person_detected == True
    else:
        return Person_detected == False

def temp_sensor(): #Temperature and humidity sensor
    temperature = temp_sensor.read_temp_humidity()
    high_temp = False
    if temperature > 40: # High temperature detected
        return high_temp == True
    else:
        return high_temp == False
def moisture_sensor(): #Moisture sensor: To check if sprinkler is working
    moisture_value = moisture_sensor.read_sensor()
    moisture_detected = False
    if moisture_value < 300: # Moisture detected
        return moisture_detected == True
    else:
        return moisture_detected == False
    
def humidity_sensor(): #Humidity sensor: For data
    humidity_value = temp_humid_sensor.read_temp_humidity()
    print ("Humidity value: ", humidity_value)
    return humidity_value

#  OUTPUT LOGIC
def dc_motor(smoke_detected): #Door opener, dc motor control
    if smoke_detected:
        dc_motor.set_motor_speed(100)  # Turn on motor at full speed
        time.sleep(5)
    else:
        dc_motor.set_motor_speed(0)  # Turn off motor

def servo(smoke_detected): #Sprinkler, ac motor control
    if smoke_detected:
        servo.set_servo_position(90)  # Activate sprinkler
        time.sleep(5)
    else:
        servo.set_servo_position(0)  # Deactivate sprinkler



if __name__ == '__main__':
    main()