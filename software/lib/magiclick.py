import board
import time
import digitalio
import analogio
import gc
import os
import busio
import audiobusio
import audiocore
import terminalio
import keypad

import displayio
import struct
import microcontroller
import supervisor 


from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC

from adafruit_st7789 import ST7789


# gc.enable()

#spi
SPI_SCLK= board.IO5
SPI_MOSI= board.IO4
# SPI_MISO= board.IO15


#display
LCD_CS = board.IO9
LCD_DC = board.IO38
LCD_RST = board.IO10
LCD_BL = board.IO37


# key
KEY1= board.IO11
KEY2= board.IO0
KEY3= board.IO39

# battery
BATT = board.IO7



#I2C DEVICES
I2C_SCL = board.IO36
I2C_SDA = board.IO35

IOX = board.IO1


# i2s
AUDIO_SD = board.IO12
AUDIO_DATA = board.IO13
AUDIO_BCK = board.IO14
AUDIO_WS = board.IO15

def execfile(pyfile='code.py'):
    supervisor.set_next_code_file(pyfile)
    print("\033[2J",end="") #clear screen
    print("Free memory:"+str(gc.mem_free()))
    print("Next boot set to:")
    print(pyfile)
    try:
        
        gc.collect()
        exec(open(pyfile).read())
    except Exception as err:
        print(err)
    print("Program finished ...")
    print("\033[2J",end="") #clear screen



displayio.release_displays()

spi = busio.SPI(SPI_SCLK,SPI_MOSI)

while not spi.try_lock():
    pass
spi.configure(baudrate=24000000) # Configure SPI for 24MHz
spi.unlock()




i2c = busio.I2C(I2C_SCL,I2C_SDA, frequency=100000,timeout=255)

while not i2c.try_lock():
    pass 
i2c.unlock()



# i2s = audiobusio.I2SOut(AUDIO_BCK,AUDIO_WS,AUDIO_DATA)
 


# audio power,Pull SD_MODE low to place the device in shutdown
audiopwr = digitalio.DigitalInOut(AUDIO_SD)
audiopwr.direction = digitalio.Direction.OUTPUT
audiopwr.value = False   #power on




display_bus = displayio.FourWire(spi,command=LCD_DC,chip_select=LCD_CS) 

lcd_reset = digitalio.DigitalInOut(LCD_RST)
lcd_reset.direction = digitalio.Direction.OUTPUT

 
def audiopwr_on():
    audiopwr.value = True
    
def audiopwr_off():
    audiopwr.value = False    

def disp_reset():
    lcd_reset.value = True   #power on
    time.sleep(0.1)
    lcd_reset.value = False   #power off
    time.sleep(0.1)
    lcd_reset.value = True   #power on
    time.sleep(0.1)

disp_reset()

display = ST7789(display_bus, width=128, height=128, colstart=2,rowstart=1,backlight_pin=LCD_BL,)

display.bus.send(0x36, struct.pack(">h", 0xc8))
display.show(None)
display.root_group[0].hidden = False
display.root_group[1].hidden = True # logo
display.root_group[2].hidden = True # status bar

imu = LSM6DS3TRC(i2c)

keys = keypad.Keys((KEY1,KEY2,KEY3,), value_when_pressed=False, pull = True)
# Clear any queued key transition events. Also sets overflowed to False.
def clearkey():
    keys.events.clear()
    
# Create an event we will reuse over and over.
event = keypad.Event()

def getkey():     
    if keys.events.get_into(event):
        if event.pressed:
            # print(event)
            return event.key_number
        
        if event.released:
            return event.key_number+10
            # print(event)
            pass
    return -1

def returnMainPage():
    display.show(None)
    lcd_reset.value = False
    supervisor.set_next_code_file("code.py")
    supervisor.reload()





# 以下代码未验证
'''
class KeyHandler:
    def __init__(self):
        self.key_state = keypad.Keys.RELEASED
        self.key_press_time = 0
        self.key_press_count = 0

    def handle_key(self, key):
        if key == keypad.Keys.PRESSED:
            self.key_press_time = time.monotonic()
            self.key_press_count += 1
        elif key == keypad.Keys.RELEASED:
            elapsed_time = time.monotonic() - self.key_press_time
            if elapsed_time < 0.5:
                print("Short press")
            elif elapsed_time >= 0.5 and elapsed_time < 1.0:
                print("Long press")
            elif elapsed_time >= 1.0 and elapsed_time < 2.0:
                print("Double press")
            elif elapsed_time >= 2.0:
                print("Triple press")
            self.key_press_time = 0
            self.key_press_count = 0

key_handler = KeyHandler()


while True:
    key_state = keypad.get_key_state()
    if key_state != key_handler.key_state:
        key_handler.handle_key(key_state)
        key_handler.key_state = key_state
    time.sleep(0.001)


'''

