# importing necessary libraries
from psychopy import visual, core

# create a window
mywin = visual.Window(monitor="testMonitor", units="deg", rgb=0)

# create some stimuli
grating = visual.GratingStim(win=mywin, mask="circle", size=4, pos=[0,0], sf=1, contrast=0.6, phase=(0.0, 0.0))
fixation = visual.GratingStim(win=mywin, pos=[0,0], sf=0, rgb=0)

# calculate framerate of monitor setup
frame_rate = int(mywin.getActualFrameRate())
print(frame_rate)

# 60 frames = 1 second
# frame/Hz value
# 30 frames = 1 hz
# 15 frames = 2 hz
# 7.5 frames = 4 hz
# 5 frames = 6 hz
# 3 frames = 10 hz
# 2.5 frames = 12 hz
# 2 frames = 15 hz
# 1 frame = 30 hz
frame = 30

# duration in seconds for stimulus & buffer
seconds_stim = 10
seconds_buf = 1

# allow stimulus to buffer
for frameN in range(frame_rate*seconds_buf):
    fixation.draw()
    mywin.update()

for frameN in range(frame_rate*seconds_stim):
    if (frameN % (frame*2)) >= frame:
        grating.draw()
    mywin.flip()

# allow stimulus to buffer
for frameN in range(frame_rate*seconds_buf):
    fixation.draw()
    mywin.update()

# close window
mywin.close()
core.quit()
