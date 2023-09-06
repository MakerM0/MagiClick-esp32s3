'''
fist.py
ICON from https://icons8.com/

v0.1.0
    20230801
    first release
    
'''




from magiclick import *

import supervisor
import os
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import adafruit_imageload
import gifio
import struct

from random import randint
import audiocore
import array
import math


# Generate one period of sine wav, 8ksps 440 Hz sin wave:
length = 8000 // 1024
sine_wave = array.array("h", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * (2 ** 15))
sine_wave = audiocore.RawSample(sine_wave)

def playwave():
    audiopwr_on()
    i2s = audiobusio.I2SOut(AUDIO_BCK,AUDIO_WS,AUDIO_DATA)
    i2s.play(sine_wave, loop=True)
    time.sleep(0.5)
    i2s.stop()
    i2s.deinit()
    audiopwr_off()
    pass




 
odg = gifio.OnDiskGif('images/fist/icons8-fist.gif')
print(odg.frame_count)
start = time.monotonic()
next_delay = odg.next_frame() # Load the first frame
end = time.monotonic()
overhead = end - start
#  
# print(overhead)

# odg.palette.make_transparent(0)
face = displayio.TileGrid(
    odg.bitmap,
    pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565_SWAPPED),
    x=8,
    y=8
    )


splash = displayio.Group(scale=2)
rect = Rect(0, 0, 64, 64, fill=0xffffff)
splash.append(rect)

splash.append(face)
display.show(splash)
display.refresh()


gif_files=['icons8-fist.gif','icons8-fist (1).gif','icons8-fist (2).gif']
index=0


def draw_gif(filename):
    splash.pop()
    odg = gifio.OnDiskGif('images/fist/'+filename)
    cnt =odg.frame_count-6
    print(odg.frame_count)
    start = time.monotonic()
    next_delay = odg.next_frame() # Load the first frame
    end = time.monotonic()
    overhead = end - start
     
    print(overhead)

    # odg.palette.make_transparent(0)
    face = displayio.TileGrid(
        odg.bitmap,
        pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565_SWAPPED),
        x=8,
        y=8
        )
    splash.append(face)
    while cnt:
        time.sleep(max(0, next_delay - overhead))
        next_delay = odg.next_frame()
        cnt-=1
    
 



# Display repeatedly.
while True:
    key = getkey()
    if key==0:
        index=randint(0,2)
        
        draw_gif(gif_files[index])
        playwave()
        gc.collect()
        print(gc.mem_free())
    elif key==2:
        returnMainPage()
    time.sleep(0.2)
 

