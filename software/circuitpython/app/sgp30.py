'''

v0.1.0
    20230917
    first release
    
'''

from magiclick import *
import adafruit_sgp30
import os
 
import time
 
import board
import displayio
import terminalio
 
# import adafruit_imageload
from adafruit_display_text import bitmap_label
 


# Define time interval between requests
time_interval = 1  # set the time interval to 1s
 

sgp30 =None
 
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
try :
    sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
except :
    print("no sensor")
    time.sleep(1)
    returnMainPage()

#the get serial ID command returns 3 words, and every word is followed by an 8-bit CRC checksum. Together the 3 words constitute a unique serial ID with a length of 48 bits.
print("SGP30 serial #", [hex(i) for i in sgp30.serial])
# Baseline values: eCO2 = 0x8cb8, TVOC = 0x9c87
sgp30.set_iaq_baseline(0x8973, 0x8AAE)
sgp30.set_iaq_relative_humidity(celsius=30.0, relative_humidity=50)

elapsed_sec = 0

# while True:
#     print("eCO2 = %d ppm \t TVOC = %d ppb" % (sgp30.eCO2, sgp30.TVOC))
#     time.sleep(1)
#     elapsed_sec += 1
#     if elapsed_sec > 10:
#         elapsed_sec = 0
#         print(
#             "**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
#             % (sgp30.baseline_eCO2, sgp30.baseline_TVOC)
#         )




display.show(None)
TERMINAL_HEIGHT=display.height+20
display.root_group.scale = 1
    
display.root_group[0].hidden = False
display.root_group[1].hidden = True # logo
display.root_group[2].hidden = True # status bar
supervisor.reset_terminal(display.width,TERMINAL_HEIGHT)
display.root_group[0].y = 0


display.show(display.root_group)

group = displayio.Group()

# Create label for displaying temperature data
stock_area = bitmap_label.Label(terminalio.FONT, scale=2)
stock_area.anchor_point = (0.5, 0)
stock_area.anchored_position = (display.width // 2, 0)
stock_area.text='0'


# Create label for displaying temperature data
text_area = bitmap_label.Label(terminalio.FONT, scale=2)
# text_area.x=10
# text_area.y=50
text_area.anchor_point = (0.5,0)
text_area.anchored_position = (display.width // 2, 20)

text_area2 = bitmap_label.Label(terminalio.FONT, scale=2)
# text_area2.x=10
# text_area2.y=90
text_area2.anchor_point = (0.5, 0)
text_area2.anchored_position = (display.width // 2, 70)
# Create main group to hold all display groups
main_group = displayio.Group()
main_group.append(group)
main_group.append(stock_area)
main_group.append(text_area)
main_group.append(text_area2)
# Show the main group on the display
display.show(main_group)

 
 

def disp_sgp30():
    eco2 = sgp30.eCO2
    tvoc= sgp30.TVOC
    print("eCO2 = %d ppm \t TVOC = %d ppb" % (sgp30.eCO2, sgp30.TVOC))
    if eco2<700:
        text_area.color=0x00ff00
        text_area2.color=0x00ff00
    else:
        text_area.color=0xff0000
        text_area2.color=0xff0000


    text_area.text="eCO2\n%d ppm " % (eco2)
    text_area2.text= "TVOC\n%d ppb" % (tvoc)


disp_sgp30()
 
now = time.monotonic()
old = now

while True:
    now =  time.monotonic()
    if (now-old) >= time_interval:
        old = time.monotonic()
        
        disp_sgp30()
        gc.collect()
        
        elapsed_sec += 1
        if elapsed_sec > 10:
            elapsed_sec = 0
            print(
                "**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
                % (sgp30.baseline_eCO2, sgp30.baseline_TVOC)
            )
        
    time.sleep(0.2)
    
    key = getkey()
    if key>0:
        print(key)
    if key==0:
         
        clearkey()
    elif key==2 or key==1:
        print('exit')
        returnMainPage() 
     
                
    acceleration = imu.acceleration
    if acceleration[2] > 8.0:
        returnMainPage()   










