import time
from threading import Thread
import queue
import RFID
import Fire_detection
from hal import hal_rfid_reader

#def init():
    #Fire_detection.init()



def main():
    Fire_detection.initialise()

    #while True:
     #   if RFID.RFID_reader():
      #      print("RFID PRESENT - System Activated")
       # else:
        #    print("Waiting for RFID card...")
        #time.sleep(2) 
    
    

    while True:
        if Fire_detection.fire_detected():
            print("FIRE DETECTED! Initiate emergency procedures.")
        else:
            print("No fire detected.")
        time.sleep(2)  # Check every 2 seconds
    

   

if __name__ == '__main__':
    main()