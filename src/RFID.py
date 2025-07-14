import time
from threading import Thread
import queue
from hal import hal_rfid_reader as rfid_reader

def intialise():
    #initialization of HAL modules
    rfid_reader.init()
    
def RFID_reader(): #Start button
    Start_button = False
    id = rfid_reader.read_id_no_block()
    if id != "None": # RFID card detected
        return Start_button == True
    else:
        return Start_button == False