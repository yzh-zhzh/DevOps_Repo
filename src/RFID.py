import time
from threading import Thread
import queue

from hal import hal_rfid_reader

def RFID_reader():
    id = hal_rfid_reader.read_id_no_block()
    if id is not None:
        print(f"RFID card detected! ID = {id}")
        return True
    else:
        print("No RFID card detected")
        return False
       