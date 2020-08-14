# importing necessary libraries
from psychopy import visual, core
import random
import numpy
import platform
import os

from datetime import datetime
Date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

if "Darwin" in platform.system():
    def read_channel():
      adc = random.randrange(1023)
      return adc
else:
    import spidev
    # Open SPI bus
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz=15600000

    # Function to read SPI data from MCP3008 chip
    # Channel must be an integer 0-7
    def read_channel():
        channel = 0
        adc = spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
#def ConvertVolts(data,places):
  #volts = (data * 3.3) / float(1023)
  #volts = round(volts,places)
  #return volts

# analog channel
light_channel = 0

# Read the light sensor data
#light_level = read_channel(light_channel)
#light_volts = ConvertVolts(light_level,2)

# create an array
qty = 30 #max dots
cordinates = numpy.zeros((qty, 2), dtype = int)

#create a window
mywin = visual.Window([800,600], monitor="testMonitor", units="deg")

# setting the range of coordinates and how many coordinates to produce
rangeX = (-7, 7)
rangeY = (-7, 7)

# setting up function to print random coordinates
i = 0
while i<qty:
    x = random.randrange(*rangeX)
    y = random.randrange(*rangeY)
    cordinates[i, :] = [x,y]
    i += 1
numpy.savetxt('myCoordinates.csv', cordinates, delimiter=',', newline='\n')


frame_rate = mywin.getActualFrameRate()
frame_rpts = 15
stim_per_rpt = 4 
sampling_values = numpy.zeros((frame_rpts * stim_per_rpt * 2, qty), dtype = int)

for i in range (qty): # show all dots one after another
    frame_count = 0
    fixation = visual.GratingStim(win=mywin, mask="circle", size=2, pos= cordinates[i,:], sf=0, color=[-1,-1,-1], colorSpace='rgb')
    inverse_fixation = visual.GratingStim(win=mywin, mask="circle", size=2, pos= cordinates[i,:], sf=0, color=[1,1,1], colorSpace='rgb')
    
    for j in range (frame_rpts): # 15 times should give us 2 sec of flicker  
        # this next bit should take 1/60 * 8 sec, ie 7.5 Hz
        for k in range (stim_per_rpt): # show each pattern for 4 frames; sample every frame
            # create some stimuli
            fixation.draw()
            sampling_values [frame_count, i] = read_channel() 
            frame_count = frame_count + 1
            mywin.flip()
        for k in range (stim_per_rpt): # now show the opposite frame
            inverse_fixation.draw()
            sampling_values [frame_count, i] = read_channel() 
            frame_count = frame_count + 1
            mywin.flip()

# close window
mywin.close()

numpy.savetxt('myData.csv', sampling_values, delimiter=',', newline='\n')

os.rename("myData.csv", "myData" + Date + ".csv")
os.rename("myCoordinates.csv", "myCoordinates" + Date + ".csv")

print ('Frame rate is ' + str(frame_rate))
