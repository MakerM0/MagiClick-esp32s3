'''
v0.2.3
    20230913
    del fail info ...
    fix 2dian
v0.2.2
    20230824
    use ntp
v0.2.1
    20230802
    delay time:10s

v0.2.0
    20230723
    Fix unexpected breaks, i2s
    add week
    delete gif
'''




from magiclick import *
import wifi
import socketpool
import os
import rtc
import time
import audiocore
import board
import audiobusio
from adafruit_display_text import label
import adafruit_ntp
 


display.show(None)


TERMINAL_HEIGHT=display.height+20
display.root_group.scale = 1
    
display.root_group[0].hidden = False
display.root_group[1].hidden = True # logo
display.root_group[2].hidden = True # status bar
supervisor.reset_terminal(display.width,TERMINAL_HEIGHT)
display.root_group[0].y = 0


display.show(display.root_group)

print('         CLOCK  ')
print(' ')
print(' ')
print(' ')
 

 

spHour = ["12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
spMinDec = ["0", "10", "20", "30", "40", "50"]
spMinSpecial = ["11", "12", "13", "14", "15", "16", "17", "18", "19"]
spMinLow = ["1", "ai", "3", "4", "5", "6", "7", "8", "9"]


def playwave(filename):
    audiopwr_on()
    i2s = audiobusio.I2SOut(AUDIO_BCK,AUDIO_WS,AUDIO_DATA)
    try :
        wave_file = open('audio/cn_girl/{}'.format(filename), "rb")
        wave = audiocore.WaveFile(wave_file)
        i2s.play(wave)
        while i2s.playing:
            pass
        wave.deinit()
        wave_file.close()
        wave_file=None
        gc.collect()
         
    except Exception as e : 
        print (e)
    i2s.deinit()
    audiopwr_off()
    pass


def sayTimeCN(hour,  minutes):
    pm=False
    if hour>=12:
        pm=True     

#     playwave("audio/cn_girl/the time is.wav")
#     if pm:
#         playwave("afternoon.wav")
#     else:
#         playwave("morning.wav")

    hour = hour % 12

    playwave("{}.wav".format(spHour[hour]))
    playwave("dian.wav")
    
    if minutes == 0:
        pass
#         playwave("zheng.wav") 
    elif minutes <= 10 or minutes >= 20:
        playwave("{}.wav".format(spMinDec[minutes // 10]))
        if minutes % 10:
            playwave("{}.wav".format(spMinLow[(minutes % 10) - 1]))             

        playwave("fen.wav")

    else:
        playwave("{}.wav".format(spMinSpecial[minutes - 11])) 
        playwave("fen.wav")
        
        
 


if  os.getenv("WIFI_SSID")=="":
    print('Please set the wifi \r\ninformation in the \r\nsettings.toml file.')
    print('Exit after 10 seconds')
    time.sleep(1.0)
    for i in range(10):
#         print('... ')
        time.sleep(1.0)   
        
    returnMainPage()
        

# if not wifi.Radio.connected:
print(f"Connecting to \r\n[ {os.getenv('WIFI_SSID')} ]")
while not wifi.radio.connected:
    try:
        wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
    except Exception as ex:
        print(ex)
    time.sleep(0.5)
    print('.')

 

print(f"Connected to {os.getenv('WIFI_SSID')}")
print(f"My IP address: {wifi.radio.ipv4_address}")


TIME_API = "http://worldtimeapi.org/api/ip"


 


pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=8, server = "ntp1.aliyun.com")

 



try: 
    rtc.RTC().datetime = ntp.datetime
except Exception as e:
    print(e)
    pass
 
time_now = time.localtime()
print(time_now)
 
wifi.radio.stop_station()
wifi.radio.enabled=False
pool=None
requests = None
gc.collect()
 
display.show(None)
main_group = displayio.Group()



# import gifio
#  
# # display.auto_refresh = False
# 
# COL_OFFSET = 80  # The Feather TFT needs to have the display
# ROW_OFFSET = 40  # offset by these values for direct writes 
# 
# 
# odg = gifio.OnDiskGif('images/clock_1.gif')
# start = time.monotonic()
# next_delay = odg.next_frame() # Load the first frame
# end = time.monotonic()
# overhead = end - start
# 
# 
# face = displayio.TileGrid(
#     odg.bitmap,
#     pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565_SWAPPED),
#     x=COL_OFFSET,
#     y=ROW_OFFSET
#     ) 
#  
# main_group.append(face)

from adafruit_bitmap_font import bitmap_font
font_file = "fonts/LeagueSpartan-Bold-16.bdf"
font = bitmap_font.load_font(font_file)
# font = terminalio.FONT

# label
hour_label = label.Label(terminalio.FONT, color=0x00ff00, scale=6)
hour_label.anchor_point = (1.0, 0.0)
hour_label.anchored_position = (display.width-1, 0)
hour_label.text = "{:0>2d}".format(time_now.tm_hour)

minute_label = label.Label(terminalio.FONT, color=0x00ffff, scale=6)
minute_label.anchor_point = (1.0, 0.0)
minute_label.anchored_position = (display.width-1, 64)
minute_label.text = "{:0>2d}".format(time_now.tm_min)

# gc_label = label.Label(terminalio.FONT, color=0xff00ff, scale=1)
# gc_label.anchor_point = (0.5, 0.0)
# gc_label.anchored_position = (display.width / 2+40, 110)
# gc_label.text = "{}KB".format(gc.mem_free()/1024)



main_group.append(hour_label)
main_group.append(minute_label)
# main_group.append(gc_label)

WEEK_COLOR_NOW = 0xCCCCCC
WEEK_COLOR_NOTNOW=0x444444
week_id = time_now.tm_wday
week_label=[]
weeks = ("MON","TUE","WED","THU","FRI","SAT","SUN")
for i in range(7):
    wlabel = label.Label(font, color=WEEK_COLOR_NOTNOW, scale=1)
    wlabel.anchor_point = (0.0, 0.0)
    wlabel.anchored_position = (0, i*19)
    wlabel.text = f"{weeks[i]}"
    week_label.append(wlabel)
    main_group.append(wlabel)
    
week_label[week_id].color = WEEK_COLOR_NOW

# print(time_now.tm_wday)
# print(week_id)

display.show(main_group)

# sayTimeCN(2, 2) 
sayTimeCN(time_now.tm_hour, time_now.tm_min) 
# display.refresh()  

now = time.monotonic()
old = now
clearkey()
key=-1
acceleration = imu.acceleration
#
f_time_sayed=False
while True:
    now =  time.monotonic()
    if (now-old) >= 10.0:
        old = time.monotonic()
        time_now = time.localtime()
#         print(time_now)
        gc.collect()
        hour_label.text = "{:0>2d}".format(time_now.tm_hour)
        minute_label.text = "{:0>2d}".format( time_now.tm_min)
#         gc_label.text = "{}KB".format(gc.mem_free()/1024)
        
        if time_now.tm_wday != week_id:
#             print(time_now.tm_wday)
#             print(week_id)
            week_label[week_id].color = WEEK_COLOR_NOTNOW
            week_label[time_now.tm_wday].color = WEEK_COLOR_NOW
            weekid = time_now.tm_wday
            
        
        if time_now.tm_min==0:            
            if time_now.tm_hour>7 and time_now.tm_hour<24:
                if f_time_sayed ==False:
                    f_time_sayed=True
                    sayTimeCN(time_now.tm_hour, time_now.tm_min)
        else:
            if f_time_sayed:
                f_time_sayed = False
            
        
    # print(random.randint(0,99))    
        
    # Sleep for the frame delay specified by the GIF,
# minus the overhead measured to advance between frames.
#     time.sleep(max(0, next_delay - overhead))
#     odg.next_frame()
    
    time.sleep(0.2)
#     print(gc.mem_free())
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
                
             
 
         

gc.collect()         
display.show(None)        
pass









