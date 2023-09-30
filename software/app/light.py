'''

v0.1.0
    20230917
    first release
    
'''

from magiclick import *
 
 
import adafruit_bh1750 
import time
 
import board
import displayio
import terminalio
 
# import adafruit_imageload
from adafruit_display_text import bitmap_label
 


# Define time interval between requests
time_interval = 1  # set the time interval to 1s



 

sensor =None
 
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
try :
    sensor = adafruit_bh1750.BH1750(i2c)
except :
    print("no sensor")
    time.sleep(1)
    returnMainPage()
    

print(sensor)

    
# display
display.show(None)


group = displayio.Group()

# Create label for displaying temperature data
title_area = bitmap_label.Label(terminalio.FONT, scale=2)
title_area.anchor_point = (0.5, 0)
title_area.anchored_position = (display.width // 2, 10)
title_area.text='Bh1750'
title_area.color = 0x7f7f70

# Create label for displaying temperature data
text_area = bitmap_label.Label(terminalio.FONT, scale=4 )
# text_area.x=10
# text_area.y=50
text_area.anchor_point = (0.5,0.5)
text_area.color = 0x0fff00
text_area.anchored_position = (display.width // 2, display.height // 2)

text_area2 = bitmap_label.Label(terminalio.FONT, scale=2)
# text_area2.x=10
# text_area2.y=90
text_area2.anchor_point = (0.5, 0)
text_area2.anchored_position = (display.width // 2, 90)
text_area2.text='Lux'
text_area2.color=0x85f555

# Create main group to hold all display groups
main_group = displayio.Group()
main_group.append(group)
main_group.append(title_area)
main_group.append(text_area)
main_group.append(text_area2)
# Show the main group on the display
display.show(main_group)


while True:
    print("%.1f Lux" % sensor.lux)
    text_area.text = "%d" % sensor.lux
    time.sleep(time_interval)

