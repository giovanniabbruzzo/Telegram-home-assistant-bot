import smbus2# Used to read 2 Bytes
import smbus # Used to read 1 Byte
import time


I2C_PORT = 1 # Port of  the I2C
bus_16 = smbus2.SMBus(I2C_PORT) # Create the I2C bus 16-bit
bus_8 = smbus.SMBus(I2C_PORT) # Create the I2C bus 8-bit

TMP116_I2C_ADDRESS = 0x49 # I2C address
# Registers
TEMP_REG = 0x00 # Temperature register
CONF_REG = 0x01 # Configuration register
DEV_ID_REG = 0x0F # Device register

# Configurations
TMP116_NO_AVG = 0x00
TMP116_CC = 0x0000 #Continuous conversion mode
TMP116_SHUTDOWN = (0x0001<<10)
TMP116_ONESHOT = (0x0002<<10)
TMP116_AVG64 = (0x0003<<5)

MIN_TEMPERATURE_ALERT = 16 # Under this value the bot will send an alert


## Read two Bytes from register reg of the TMP116 sensor
# @param reg register at which to read the data from 
# @return the list with the data [MSB, LSB]
def read_word(reg):
    return bus_16.read_i2c_block_data(TMP116_I2C_ADDRESS, reg, 16)

## Read one Byte from register reg of the TMP116 sensor
# @param reg register at which to read the data from 

# @return the Byte
def read_byte(reg):
    return bus_8.read_byte_data(TMP116_I2C_ADDRESS, reg)

## Write one Byte of data data in the register reg
# @param reg register at which to read the data from 
# @param data data to write 
def write_byte(reg, data):
    bus_16.write_byte_data(TMP116_I2C_ADDRESS, reg, data)

## Initialize 
def TMP116_init():
    try:
        data = read_word(DEV_ID_REG)
        data_h = int(data[0])
        data_l = int(data[1])
    except:
        print("Error!")
        exit()
        
    if data_h == 0x11 and data_l == 0x16:
        # Start with shutdown sensor for configuration
        config = TMP116_AVG64|TMP116_SHUTDOWN|0x02
        write_byte(CONF_REG, config)
    else:
        print("Sensor not found")

def convert_temperature(raw_data):
    hi = int(raw_data[0])
    lo = int(raw_data[1])
    if hi & 0x80:
        return -1*float((hi<<8)+(lo&0xFF)+1.0)*0.0078125
    else:
        return float((hi<<8)+(lo&0xFF))*0.0078125

def is_new_day(prev_time,current_time):
    if int(current_time[:2]) > int(prev_time[:2]):
        return True
    else:
        return False
 
def read_temperature():
    # Set for one reading
    config = TMP116_AVG64|TMP116_SHUTDOWN|0x02|TMP116_ONESHOT
    write_byte(CONF_REG, config)
    time.sleep(0.1) # Wait 0.1 s
    data_read = read_word(TEMP_REG)
    return round(convert_temperature(data_read),2)
