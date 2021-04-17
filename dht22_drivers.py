import adafruit_dht
import board

# dht22 variables connected at pin 8 or GPIO14
sensor = adafruit_dht.DHT22(board.D17)

#support functions
def getTemp():
    return sensor.temperature

def getHum():
    return sensor.humidity