from main import smoke_detector, IR_sensor, LDR_sensor, RFID_reader, Ultrasonic_sensor
def test_smoke_detector(): 
    # Test case where both sensors detect smoke
    assert smoke_detector(True, True) == True
    
    # Test case where one sensor does not detect smoke
    assert smoke_detector(True, False) == False
    assert smoke_detector(False, True) == False
    
    # Test case where neither sensor detects smoke
    assert smoke_detector(False, False) == False
def test_IR_sensor():
    # Test case where smoke is detected
    assert IR_sensor() == True
    
    # Test case where no smoke is detected
    assert IR_sensor() == False

def test_LDR_sensor():
    # Test case where smoke is detected
    assert LDR_sensor() == True
    
    # Test case where no smoke is detected
    assert LDR_sensor() == False

def test_RFID_reader():
    # Test case where RFID card is detected
    assert RFID_reader() == True
    
    # Test case where no RFID card is detected
    assert RFID_reader() == False
