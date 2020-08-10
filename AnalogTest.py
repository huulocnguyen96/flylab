# importing necessary libraries
from psychopy import visual, core
import random
import spidev
import numpy

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=15600000 

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def read_channel(channel):
 adc = spi.xfer2([1,(8+channel)<<4,0])
 data = ((adc[1]&3) << 8) + adc[2]
 return data


while True:
    print('Raw ADC Value: ', read_channel(0))
