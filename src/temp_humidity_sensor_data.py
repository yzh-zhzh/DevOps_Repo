from hal import hal_temp_humidity_sensor as temp_humidity
from time import sleep

def read_data(): 
    temp_humidity.init() 
    data = temp_humidity.read_temp_humidity()
    temperature = data[0]
    humidity = data[1]

    return temperature, humidity

def temperature_condition(current_temp) : 
    if current_temp >= 20 : 
        return "Fire Detected"
    elif current_temp >= 10 : 
        return "Warning"
    else : 
        return "Normal"

def humidity_condition(current_humid): 
    if current_humid < 20 : 
        return "Low humidity"
    else : 
        return "Normal"

def temp_humid_fire_condition(Temp,Humid):
    if (Temp == "Fire Detected") or (Temp == "Warning" and Humid == "Low humidity"): 
        return "FIRE"
    else : 
        return "NORMAL"
def main() : 
     while True : 
        temp, humid = read_data()
        temp_condition = temperature_condition(temp)
        humid_condition = humidity_condition(humid)
        return(temp_humid_fire_condition(temp_condition,humid_condition))

if __name__ == '__main__':
    main()
            