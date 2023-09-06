'''
v0.2.0
    20230723
    add bmp

'''


from magiclick import *
import adafruit_imageload
import asyncio
import random 
import terminalio
 



class Dice:
    def __init__(self):
        self.value=0
        self.f_start=False
        self.f_loop = False
        self.f_stop = False
        self.f_destroy =False
        
    def roll(self):
        self.value = random.randint(0,5)
        
    
    def start(self):
        pass
    
    def stop(self):
        pass
        
        
display.show(None) 
 


# Make the display context
splash = displayio.Group()


# image, palette = adafruit_imageload.load('/images/dice/dice_.png')
image, palette = adafruit_imageload.load('/images/dice/dice.bmp',bitmap = displayio.Bitmap,palette = displayio.Palette)
# Set the transparency index color to be hidden
# palette.make_transparent(0)

tile_grid = displayio.TileGrid(image,pixel_shader = palette,
                               tile_width = 100,
                               tile_height = 100,
                               width = 1,
                               height = 1)
tile_grid.x = display.width//2-50 
tile_grid.y = display.height//2-50


splash.append(tile_grid)
display.show(splash)

   
        

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
             
            tile_grid[0] = dice.value
            tile_grid.x = display.width//2-50 +random.randint(-10,10)
            tile_grid.y = display.height//2-50+random.randint(-10,10)
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
    



