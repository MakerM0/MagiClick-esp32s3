'''

v0.1.0
    20230913
    first release
    
'''

from magiclick import *

import os
import ssl
import time
import wifi
import board
import displayio
import terminalio
import socketpool
import adafruit_requests
# import adafruit_imageload
from adafruit_display_text import bitmap_label
import json


# Define time interval between requests
time_interval = 300  # set the time interval to 5 minutes
stock_code = 'sh688018'  #espressif








display.show(None)
TERMINAL_HEIGHT=display.height+20
display.root_group.scale = 1
    
display.root_group[0].hidden = False
display.root_group[1].hidden = True # logo
display.root_group[2].hidden = True # status bar
supervisor.reset_terminal(display.width,TERMINAL_HEIGHT)
display.root_group[0].y = 0


display.show(display.root_group)


print('         Stock  ')
print(' ')
print(' ')
print(' ')


print(f"Connecting to \r\n[ {os.getenv('WIFI_SSID')} ]")
# Initialize Wi-Fi connection
try:
    wifi.radio.connect(
        os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD")
    )
    print("Connected to %s!" % os.getenv("WIFI_SSID"))
# Wi-Fi connectivity fails with error messages, not specific errors, so this except is broad.
except Exception as e:  # pylint: disable=broad-except
    print(
        "Failed to connect to WiFi. Error:", e, "\nBoard will hard reset in 30 seconds."
    )
    
    
# Create a socket pool and session object for making HTTP requests
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# # Set location and units for weather data
# 
# WEATHERKEY = os.getenv("WEATHER_KEY")
# if WEATHERKEY =="":    
#     WEATHERKEY = 'ctpe2272nswh94og'
    








 

group = displayio.Group()

# Create label for displaying temperature data
stock_area = bitmap_label.Label(terminalio.FONT, scale=2)
stock_area.anchor_point = (0.5, 0)
stock_area.anchored_position = (display.width // 2, 0)
stock_area.text=stock_code


# Create label for displaying temperature data
text_area = bitmap_label.Label(terminalio.FONT, scale=3)
# text_area.x=10
# text_area.y=50
text_area.anchor_point = (0.5,0)
text_area.anchored_position = (display.width // 2, 40)

text_area2 = bitmap_label.Label(terminalio.FONT, scale=2)
# text_area2.x=10
# text_area2.y=90
text_area2.anchor_point = (0.5, 0)
text_area2.anchored_position = (display.width // 2, 90)
# Create main group to hold all display groups
main_group = displayio.Group()
main_group.append(group)
main_group.append(stock_area)
main_group.append(text_area)
main_group.append(text_area2)
# Show the main group on the display
display.show(main_group)



def get_stock(stock):
    try:
        response = requests.get('http://hq.finance.ifeng.com/q.php?l='+stock )
        info = json.loads(response.text[11:-3])
#         print(info)
 
        print(info[stock][0])#当前价
        print(info[stock][1])#开盘价
        print(info[stock][2])#涨跌量
        print(info[stock][3])#涨跌幅

        return info[stock][0],info[stock][1],info[stock][2],info[stock][3]
    except:

        return 0,0,0,0
 

def disp_stock(price):
    if price[2]<0:
        text_area.color=0x00ff00
        text_area2.color=0x00ff00
    else:
        text_area.color=0xff0000
        text_area2.color=0xff0000


    text_area.text=str(price[0])
    text_area2.text= '{:.2f}%'.format(price[3])

price = get_stock(stock_code)
disp_stock(price)
 
now = time.monotonic()
old = now

while True:
    now =  time.monotonic()
    if (now-old) >= time_interval:
        old = time.monotonic()
        price = get_stock(stock_code)
        disp_stock(price)
        gc.collect()
        
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










