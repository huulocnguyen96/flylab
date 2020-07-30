# importing necessary libraries
from psychopy import visual, core
import random

#create a window
mywin = visual.Window([800,600], monitor="testMonitor", units="deg")

# setting the range of coordinates and how many coordinates to produce
rangeX = (-7, 7)
rangeY = (-7, 7)
qty = 1

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
print(cords)

# create some stimuli
fixation = visual.GratingStim(win=mywin, mask="circle", size=2, pos= cords, sf=0, rgb=-1)

# draw the stimuli and update the window
fixation.draw()
mywin.update()

# pause (in s)
core.wait(5)
