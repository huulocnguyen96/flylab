# importing necessary libraries
from psychopy import visual, core
import random
import numpy
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.CE0)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

# create an array
cordinates = numpy.array([])
sampling_value = numpy.array([])

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
    new_cords = numpy.append(cordinates, cords)

    for i in range (4):
        # create some stimuli
        fixation = visual.GratingStim(win=mywin, mask="circle", size=2, pos= cords, sf=0, rgb=-1)
        inverse_fixation = visual.GratingStim(win=mywin, mask="circle", size=2, pos= cords, sf=0, rgb=0)

        for frameN in range(frame_rate * seconds_stim):
            if (frameN % (frame * 2)) >= frame:
                fixation.draw()
                new_sampling_values = numpy.append(sampling_value, str(chan.voltage))
            else:
                inverse_fixation.draw()
                new_sampling_values = numpy.append(sampling_value, str(chan.voltage))
            mywin.flip()

print(new_cords, file=open("cords.txt"))
print(new_sampling_values, file=open("sampling.txt"))
