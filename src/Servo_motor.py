from hal import hal_servo as servo

def fire_alert_activation() : 
    servo.init() 
    servo.set_servo_position(90) 
    print("Activated!")
    return True # activated

def deactivation() : 
    servo.init() 
    servo.set_servo_position(0) 
    print("Deactivated!") 
    return True #deactivated

def main() : 
    if sth == sth : 
        fire_alert_activation
    elif sth == sth and sth == sth : 
        deactivation

if __name__ == '__main__':
    main()
            
