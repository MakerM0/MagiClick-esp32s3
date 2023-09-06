'''
v0.2.0
    add mac command+F3 进入桌面,未完成


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


'''

The icons is from here  https://icons8.com/


Modify the keymap to implement more functionality

---------------------------------------------------------
| image | text | keycode1 | keycode2 | keycode3 | ..... |
---------------------------------------------------------

keycode
https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html

'''
MAC = False
# Choose the correct modifier key for Windows or Mac.
# Comment one line and uncomment the other.

if not MAC:    
    MODIFIER = Keycode.CONTROL  # For Windows
else:
    MODIFIER = Keycode.COMMAND  # For Mac

keymap=(
    ('desktop_96px.png','Desktop',Keycode.FN,Keycode.F11) if MAC else ('desktop_96px.png','Desktop',Keycode.GUI,Keycode.D),
    ('explorer_96px.png','explorer',Keycode.GUI,Keycode.E),
    ('system_96px.png','Taskmgr',MODIFIER,Keycode.SHIFT,Keycode.ESCAPE),
    (None,'Cut',MODIFIER,Keycode.X),
    (None,'Copy',MODIFIER,Keycode.C),
    (None,'Paste',MODIFIER,Keycode.V),    
    ('f5_96px_.png','F5',Keycode.F5),
        )

 
ICON_WIDTH=96
ICON_HEIGHT=96

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
trytime=0 
while not supervisor.runtime.usb_connected:
    time.sleep(1.0)
    print(" no usb connected")
    trytime+=1
    if trytime>=5:
        returnMainPage()
        
     


LEN = len(keymap)
index=0

font =terminalio.FONT
# font = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf")

display.show(None)
main_group = displayio.Group()
display.show(main_group)
# label 
keylabel = label.Label(font, color=0x00ff00, scale=4)
keylabel.anchor_point = (0.5, 0.5)
keylabel.anchored_position = (display.width // 2, display.height // 2)
keylabel.text = "" 


main_group.append(keylabel)


#image, 8bit png
transparent_img = displayio.Bitmap(ICON_WIDTH,ICON_HEIGHT,1)
palette = displayio.Palette(1)
palette[0]=0x000000
# Set the transparency index color to be hidden
palette.make_transparent(0)
tile_grid = displayio.TileGrid(transparent_img,pixel_shader = palette)
tile_grid.x = display.width // 2 - tile_grid.tile_width // 2
tile_grid.y = display.height // 2 - tile_grid.tile_height // 2 - 20

main_group.append(tile_grid)







def draw_img_or_text():
    if keymap[index][0] != None:
        try:
            image, palette = adafruit_imageload.load("/images/unikey/"+keymap[index][0])
            palette.make_transparent(0)
            tile_grid.bitmap = image
            tile_grid.pixel_shader = palette
            keylabel.scale=2
            keylabel.anchored_position = (display.width // 2, 105)
            keylabel.text =keymap[index][1]
        except Exception as e:
            print (e)            
            pass
    else:
        tile_grid.bitmap = transparent_img
        keylabel.scale=4
        keylabel.anchored_position = (display.width // 2,  display.height // 2)
        keylabel.text = "\n".join(wrap_text_to_lines(keymap[index][1], 5))
        

draw_img_or_text()

display.show(main_group)



kbd = Keyboard(usb_hid.devices)


 
print(keymap)      
while True:
    key = getkey()
    
    if key==0:
        kbd.send(*keymap[index][2:])

    elif key==1:
        index -= 1
        if index<0:
            index=LEN-1 
        draw_img_or_text()
        pass
 
        
    elif key==2:
        index += 1
        if index>=LEN:
            index=0 
        draw_img_or_text()
        pass
    
    acceleration = imu.acceleration
    if acceleration[2] > 8.0:
        returnMainPage()
         
 
    
    time.sleep(0.1)
    
    
    



