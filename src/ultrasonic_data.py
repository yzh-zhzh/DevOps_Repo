from hal import hal_usonic as usonic 

def read_data() : 
    usonic.init() 
    result = usonic.get_distance() 
    return result 
    
def detect_presence(distance) : 
    if distance < 100 : 
        return True #Presence Detected
    else : 
        return  False # No presence detected

def main() : 
    while True : 
        distance = read_data()
        return (detect_presence(distance))


if __name__ == '__main__':
    main()
            