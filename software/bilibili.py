'''

v0.1.0
    20230723
    
'''
import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_display_text import label, wrap_text_to_lines
from adafruit_bitmap_font import bitmap_font
import adafruit_imageload
from magiclick import *

import supervisor




# Choose the correct modifier key for Windows or Mac.
# Comment one line and uncomment the other.
MODIFIER = Keycode.CONTROL  # For Windows
# MODIFIER = Keycode.COMMAND  # For Mac

 

 
 
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
trytime=0 
while not supervisor.runtime.usb_connected:
    time.sleep(1.0)
    print(" no usb connected")
    trytime+=1
    if trytime>=5:
        returnMainPage()
        
     
  
 

display.show(None)


# Set up display a default image 
bitmap = displayio.OnDiskBitmap("/images/bilibili/yijiansanlian.bmp")
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

group = displayio.Group()
group.append(tile_grid)

# Create main group to hold all display groups
main_group = displayio.Group()
main_group.append(group)
 
# Show the main group on the display
display.show(main_group)


kbd = Keyboard(usb_hid.devices)

     
while True:
    key = getkey()
    
    if key==0:
        kbd.press(Keycode.Q)
        time.sleep(2.5)
        kbd.release_all()
        clearkey()

     
    
    acceleration = imu.acceleration
    if acceleration[2] > 8.0:
        returnMainPage()
         
 
    
    time.sleep(0.2)
    
    
    




