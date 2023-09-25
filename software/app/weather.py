'''
v0.2.0
    20230725
    add get_weather()
        gc.collect()

v0.1.0
    20230723
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
import adafruit_imageload
from adafruit_display_text import bitmap_label

display.show(None)
TERMINAL_HEIGHT=display.height+20
display.root_group.scale = 1
    
display.root_group[0].hidden = False
display.root_group[1].hidden = True # logo
display.root_group[2].hidden = True # status bar
supervisor.reset_terminal(display.width,TERMINAL_HEIGHT)
display.root_group[0].y = 0


display.show(display.root_group)


print('         Weather  ')
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

# Set location and units for weather data

WEATHERKEY = os.getenv("WEATHER_KEY")
if WEATHERKEY =="":    
    WEATHERKEY = 'ctpe2272nswh94og'
    
LOCATION = os.getenv("LOCATION")
if LOCATION=="":
    LOCATION = 'sanya'
    
UNITS = "c"
LANGUAGE = 'en'

print("Getting weather for {}".format(LOCATION))

# Set up the URL for fetching weather data
DATA_SOURCE = (
    "http://api.seniverse.com/v3/weather/now.json?"
    + "key="
    + WEATHERKEY
    + "&location="
    + LOCATION
    + "&language="
    + LANGUAGE
    + "&unit="
    + UNITS   
)

# Define time interval between requests
time_interval = 1800  # set the time interval to 30 minutes





# Set up display a default image 
#image, 8bit png
image, palette = adafruit_imageload.load("/images/weather/icons8-sunny-64_.png")
# Set the transparency index color to be hidden
palette.make_transparent(0)

tile_grid = displayio.TileGrid(image,pixel_shader = palette)
tile_grid.x = display.width // 2 - tile_grid.tile_width // 2
tile_grid.y = display.height // 2 - tile_grid.tile_height // 2

group = displayio.Group()
group.append(tile_grid)

# Create label for displaying temperature data
text_area = bitmap_label.Label(terminalio.FONT, scale=2)
text_area.anchor_point = (0.5, 0.5)
text_area.anchored_position = (display.width // 2, display.height // 2)

# Create main group to hold all display groups
main_group = displayio.Group()
main_group.append(group)
main_group.append(text_area)
# Show the main group on the display
display.show(main_group)

# Define function to get the appropriate weather icon
def get_weather_condition_icon(weather_condition):
    if "cloud" in weather_condition.lower():
        return "/images/weather/icons8-cloudy-64_.png"
    elif "rain" in weather_condition.lower():
        return "/images/weather/icons8-rain-64_.png"
    elif "snow" in weather_condition.lower():
        return "/images/weather/icons8-snowy-64_.png"
    elif "clear" in weather_condition.lower():
        return "/images/weather/icons8-sunny-64_.png"
    else:
        return "/images/weather/icons8-sunny-64_.png"

# Define function to update the background image based on weather conditions
def set_background(weather_condition, background_tile_grid):
    bitmap_path = get_weather_condition_icon(weather_condition)    
    image, palette = adafruit_imageload.load(bitmap_path)
    palette.make_transparent(0)
    background_tile_grid.bitmap = image
    background_tile_grid.pixel_shader = palette

def get_weather():
    # Fetch weather data from OpenWeatherMap API
    print("Fetching json from", DATA_SOURCE)
    response = requests.get(DATA_SOURCE)
    print(response.json())

    # Extract temperature and weather condition data from API response
    
    current_weather_condition = response.json()["results"][0]["now"]["text"]
    current_temp = response.json()["results"][0]["now"]["temperature"]

    print("Weather condition: ", current_weather_condition)


    # Update label for displaying temperature data
    text_area.text = "{}\n\n\n     {} C".format(LOCATION, current_temp)

    # Update background image
    set_background(current_weather_condition, tile_grid)
    
 

get_weather()
now = time.monotonic()
old = now
# print(gc.mem_free())
# gc.collect()
# print(gc.mem_free())
# time.sleep(10.0)
# for i in range(10):
#     get_weather()
#     gc.collect()
#     print(gc.mem_free())
# Main loop to continuously fetch and display weather data
while True:
    now =  time.monotonic()
    if (now-old) >= time_interval:
        old = time.monotonic()
        get_weather()
        gc.collect()
        
    time.sleep(0.2)
    
    key = getkey()
    if key>0:
        print(key)
    if key==0:
        sayTimeCN(time_now.tm_hour, time_now.tm_min)
        clearkey()
    elif key==2 or key==1:
        print('exit')
        returnMainPage() 
     
                
    acceleration = imu.acceleration
    if acceleration[2] > 8.0:
        returnMainPage()   






