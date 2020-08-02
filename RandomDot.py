# importing necessary libraries
from psychopy import visual, core
import random
import spidev

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def read_channel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts

#create a window
mywin = visual.Window([800,600], monitor="testMonitor", units="deg")

# setting the range of coordinates and how many coordinates to produce
rangeX = (-7, 7)
rangeY = (-7, 7)
qty = 1

frame = 7.5
seconds_stim = 1
frame_rate = int(mywin.getActualFrameRate())

for i in range (30):

    # setting up function to print random coordinates
    cords = []
    excluded = set()
    i = 0
    while i<qty:
        x = random.randrange(*rangeX)
        y = random.randrange(*rangeY)
        if (x,y) in excluded: continue
        cords.append((x,y))
        i += 1
    print(cords, file=open("cords.txt", "a"))

    for i in range (4):
        # create some stimuli
        fixation = visual.GratingStim(win=mywin, mask="circle", size=2, pos= cords, sf=0, rgb=-1)
        inverse_fixation = visual.GratingStim(win=mywin, mask="circle", size=2, pos= cords, sf=0, rgb=0)

        for frameN in range(frame_rate * seconds_stim):
            if (frameN % (frame * 2)) >= frame:
                fixation.draw()
                #print(read_channel(channel), file=open("cords.txt", "a"))
            else:
                inverse_fixation.draw()
                #print(read_channel(channel), file=open("cords.txt", "a"))
            mywin.flip()
