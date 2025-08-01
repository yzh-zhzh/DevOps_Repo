from hal import hal_usonic as usonic 
from time import sleep
import time
from threading import Thread
def read_data() : 
    result = usonic.get_distance() 
    return result 
    
def detect_presence(distance) : 
    if distance < 100 : 
        return True #Presence Detected
    else : 
        return  False # No presence detected

def main() : 
    usonic.init()
    while True : 
        distance = read_data()
        if detect_presence(distance): 
            print("Presence Detected")
        else : 
            print("No Presence Detected")
        sleep(1)


if __name__ == '__main__':
    main()
            