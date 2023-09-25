from magiclick import *
import asyncio
import random 
import terminalio
from adafruit_display_text import label



class Dice:
    def __init__(self):
        self.value=0
        self.f_start=False
        self.f_loop = False
        self.f_stop = False
        self.f_destroy =False
        
    def roll(self):
        self.value = random.randint(0,9)
        
    
    def start(self):
        pass
    
    def stop(self):
        pass
        
        
display.show(None) 
main_group = displayio.Group()

# sprit_sheet,palette = adafruit_imageload.load('/images/gongde.bmp',bitmap = displayio.Bitmap,palette = displayio.Palette)
# palette.make_transparent(0)
# 
# spirite = displayio.TileGrid(sprit_sheet,pixel_shader=palette,
#                              width=1,
#                              height=1,
#                              tile_width=96,
#                              tile_height=96                             
#                              )
# spirite[0]=0
# spirite.x = (display.width-IMG_WIDTH)//2

# label
dice_label = label.Label(terminalio.FONT,color = 0x00ff00,scale=9)
dice_label.anchor_point = (0.5,0.5)
dice_label.anchored_position = (display.width / 2, display.height/2)
dice_label.text='0'

# main_group.append(spirite)
main_group.append(dice_label)
display.show(main_group)        
        

TICK_DICE = 3.0
# 
async def draw(dice):
    starttick=0.0
    while True:
        if dice.f_start==True:
            starttick = time.monotonic()
            dice.f_start=False            
            dice.f_loop=True
        if dice.f_loop==True:
            dice.roll()
            dice_label.text= str(dice.value)
            if time.monotonic()-starttick >= TICK_DICE:
                dice.f_loop=False
                dice.f_stop=True
        
        if dice.f_stop==True:
            dice.f_stop = False
             
        await asyncio.sleep(0.1)
        if dice.f_destroy:
            break
        
    
#     
async def imu_handle(dice):
    while True:
        acceleration = imu.acceleration
        if abs(acceleration[0]) > 20.0 or abs(acceleration[1]) > 20.0 or abs(acceleration[2]) > 20.0:
            dice.f_start=True
            
            
#         if dice.f_start:
#             if abs(acceleration[0]) < 1.0 and abs(acceleration[1]) < 1.0 and abs(acceleration[2]) < 10.0:
#                 dice.f_start=False            
        
        await asyncio.sleep(0.1)
        
        if dice.f_destroy:
            break


async def button_handle(dice):
    while True:
        await asyncio.sleep(0.2)
        key = getkey()
        
        if key==0:            
            dice.f_start=True
        
        if key==2:
            dice.f_destroy=True
            returnMainPage()
            break
         
        


# 
async def main():
    dice =Dice()
    
    
    
    
    draw_task = asyncio.create_task(draw(dice))
    imu_task = asyncio.create_task(imu_handle(dice))
    btn_task = asyncio.create_task(button_handle(dice))
    await asyncio.gather(draw_task, imu_task,btn_task)


#




asyncio.run(main())       
    
print('end')    
    

