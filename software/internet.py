 
import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_display_text.label import Label

from magiclick import *

# Define the keyboard object
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

 
  

htmls=(
    ('https://cnx-software.com/','CNX',None),
    ('https://www.szlcsc.com/','LCSC',None),
    ('https://oshwhub.com/','OSHWHub',None),
    ('https://bilibili.com/','BiliBili',None),
    
    ('https://shop113593007.taobao.com/','Espressif',None),
    ('https://oled-zjy.taobao.com/','ZJY\r\nDisplay',None),
    ('https://anxinke.taobao.com/','anxinke',None),
    )

label = Label(font=terminalio.FONT, text='', color=0x2ad5ff,background_color=0x0,scale=3)

# Open the webpage
def openweb(html):
    if not isinstance(html, str):
        raise TypeError("Parameter must be of type int")     
    keyboard.press(Keycode.CONTROL, Keycode.T)
    keyboard.release_all()
    keyboard.press(Keycode.CONTROL, Keycode.L)
    keyboard.release_all()
    layout.write(html)
    keyboard.press(Keycode.ENTER)
    keyboard.release_all()
    keyboard.press(Keycode.ENTER)
    keyboard.release_all()

def draw(title:str):
    label.text = title
    print(title)
    
    
def main():
    # Define the key to simulate
    key = Keycode.F1
    # Simulate key press
    keyboard.press(key)
    keyboard.release(key)
    # Wait for the browser to open
    time.sleep(1)
    
    index=0
    LEN = len(htmls)
    
    
    label.anchor_point = (0.0, 0.5)
    label.anchored_position = (0,64)
    label.text = htmls[index][1]
    
    group=displayio.Group(scale=1)
    group.append(label)
    display.show(group)
    
    
    while True:
        time.sleep(0.1)
        
        acceleration = imu.acceleration
        if acceleration[2] > 8.0:                
            returnMainPage()
            
        key=getkey()
        
        if key==0:
            openweb(htmls[index][0])
        if key==1:
            index +=1
            if index==LEN:
                index=0
            
            draw(htmls[index][1])
            
            
            
        if key==2:
            index -=1
            if index<0:
                index=LEN-1
            
            draw(htmls[index][1])
        
        
main()        
