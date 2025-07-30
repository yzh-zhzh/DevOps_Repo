from hal import hal_temp_humidity_sensor as temp_humidity
from time import sleep

def read_data(): 
    temp_humidity.init() 
    data = temp_humidity.read_temp_humidity()
    temperature = data[0]
    humidity = data[1]

    return temperature, humidity

def main() : 
     while True : 
        sleep(3)
        temp, humid = read_data()
        return(temp, humid)


if __name__ == '__main__':
    main()
            