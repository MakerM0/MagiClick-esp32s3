


from magiclick import *
import adafruit_imageload
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import random
import asyncio
import struct
import audiocore
display.show(None)
main_group = displayio.Group()

 


gc.collect()

IMG_WIDTH=96
IMG_HEIGHT=96
IMG_FRAME=3 #gif frames 

 

display.show(None) 
main_group = displayio.Group()


wavpath = 'audio/counter/muyu.wav'

def playwave():
    audiopwr_on()
    i2s = audiobusio.I2SOut(AUDIO_BCK,AUDIO_WS,AUDIO_DATA)
    try :
        wave_file = open(wavpath, "rb")
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

# background = Rect(0,0, display.width-1,display.height-1,fill=0xffffff)
 


 

 

img_group = displayio.Group(scale=1)

sprit_sheet,palette = adafruit_imageload.load('/images/counter/gongde.bmp',bitmap = displayio.Bitmap,palette = displayio.Palette)
 
palette.make_transparent(0)

spirite = displayio.TileGrid(sprit_sheet,pixel_shader=palette, 
                             width=1,
                             height=1,
                             tile_width=IMG_WIDTH,
                             tile_height=IMG_HEIGHT                             
                             )
palette.make_transparent(0)
spirite[0]=0
spirite.x = (display.width-IMG_WIDTH*1)//2
 
img_group.append(spirite) 





# label
cntlabel = label.Label(terminalio.FONT,color = 0x00ff00,scale=2)
cntlabel.anchor_point = (0.5,0.0)
cntlabel.anchored_position = (display.width / 2, 105)
cntlabel.text='0'

# main_group.append(background)
main_group.append(img_group)
main_group.append(cntlabel)
display.show(main_group)
 
print(gc.mem_free())
gc.collect()
print(gc.mem_free())


class Controls:
    def __init__(self):
        self.frame_cnt = 0
        self.start = False
        self.end = False
        self.cnt=0
        self.f_destroy=False
      


async def draw(controls):
    while True:
        if controls.start == False:
            if controls.end ==False:
                spirite[0] = controls.frame_cnt
 
                controls.frame_cnt+=1
                if controls.frame_cnt== IMG_FRAME:
                    controls.end = True
                    controls.frame_cnt=0
                    controls.start=False
        else:
            spirite[0] = IMG_FRAME-1   

            controls.end = False
            controls.start=False
            controls.frame_cnt=0
             
            
        await asyncio.sleep(0.02)
        
        if controls.f_destroy:
            break
        
        

async def button_handle(controls):
    while True:
        key = getkey()
        if key==0:
            controls.cnt+=1
            cntlabel.text =str(controls.cnt)
            controls.start = True
            
        
        
         
        await asyncio.sleep(0.1)
        
        if key==2 or key==1:
            controls.f_destroy=True
 
            returnMainPage()
            break
             
# async def wav_handle(controls):
#     while True:
#         if controls.start == False:
#             if controls.end ==False:
#                 playwave()
        
       
async def main():
    controls = Controls()  
    draw_task = asyncio.create_task(draw(controls))
    button_task = asyncio.create_task(button_handle(controls))
    await asyncio.gather(draw_task, button_task)
    
    
# asyncio.run(main())


def main():
    controls = Controls()
    while True:
        key = getkey()
        if key==0:
            playwave()
            controls.cnt+=1
            cntlabel.text =str(controls.cnt)
            controls.start = True
            spirite[0] = controls.frame_cnt
            for i in range(IMG_FRAME):
                spirite[0] = i
                controls.frame_cnt+=1
                if controls.frame_cnt== IMG_FRAME:
                    controls.end = True
                    controls.frame_cnt=0
                    controls.start=False
                    break
                time.sleep(0.02)
                
        elif key==2  :
            controls.f_destroy=True
 
            returnMainPage()
            break
        else:
            time.sleep(0.1)
    
main() 
 
 
display.show(None)


print('end')   












