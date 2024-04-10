'''
v0.2.2
    202411
    fix func quit order
v0.2.1
    20230925
    modify app directory
v0.2.0
    20230723
    
    The icons is from here  https://icons8.com/

'''
from magiclick import *
import alarm
import supervisor
import os
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import adafruit_imageload


class Launch:
    def __init__(self):
        self.file_list = self.get_files('/app/')
        self.file_cnt = len(self.file_list)
        self.index=0
        pass    

    def get_files(self, base):
        files = os.listdir(base)
        file_names = []
        for isdir,filetext in enumerate(files):
            if  filetext.endswith('.py'):
                if filetext  not   in  ('code.py','launch.py','boot.py'):                
                    stats = os.stat(base+filetext)
                    isdir = stats[0]&0x4000
                    if isdir:
                        pass
    #                     file_names.append((filetext,True))
                    else:
                        file_names.append(filetext)
                        
        return file_names

    # draw func 
    def draw_img(self,label,filename):
        label.text = filename.split('.')[0]
        try:
            image, palette = adafruit_imageload.load('/images/' + label.text + '_96px.png')
            palette.make_transparent(0)
            tile_grid.bitmap = image
            tile_grid.pixel_shader = palette
        except Exception as e:
            image, palette = adafruit_imageload.load('/images/python_96px.png')
            palette.make_transparent(0)
            tile_grid.bitmap = image
            tile_grid.pixel_shader = palette
            pass
 
launch = Launch()
# launch.file_list.sort()
# file_list = get_files('/')
# file_cnt = len(file_list)
print(launch.file_list)
print( launch.file_cnt)

DISPLAY_WIDTH = display.width
DISPLAY_HEIGHT = display.height

launch.index =alarm.sleep_memory[0]
 

display.show(None)

# create base display group
displaygroup = displayio.Group()
# display.root_group = displaygroup

# create display
background = Rect(0,0,DISPLAY_WIDTH-1,DISPLAY_HEIGHT-1,fill = 0x000000)
image=None
palette=None
#image, 8bit png
try:
    image, palette = adafruit_imageload.load('/images/{}_96px.png'.format(launch.file_list[launch.index].split('.')[0]))
except Exception as e:
    image, palette = adafruit_imageload.load('/images/python_96px.png')
# Set the transparency index color to be hidden
palette.make_transparent(0)

tile_grid = displayio.TileGrid(image,pixel_shader = palette)
tile_grid.x = display.width // 2 - tile_grid.tile_width // 2
tile_grid.y = 0

# label
filelabel = label.Label(terminalio.FONT,color = 0x67E1F6,scale=2)
filelabel.anchor_point = (0.5,0.0)
filelabel.anchored_position = (DISPLAY_WIDTH / 2, 100)
# filelabel.x = 10
# filelabel.y = 100
filelabel.text = launch.file_list[launch.index].split('.')[0]


displaygroup.append(background)
displaygroup.append(tile_grid)
displaygroup.append(filelabel)


display.show(displaygroup)

 

gc.collect()
print(gc.mem_free())
while True:
    time.sleep(0.1)
    key = getkey()
    if key==1:
        print('Left')
        launch.index -= 1
        if launch.index<0:
            launch.index = launch.file_cnt-1
        print(launch.index)
        launch.draw_img(filelabel,launch.file_list[launch.index])
        gc.collect()
        print(gc.mem_free())
        
    elif key==2:
        print('Right')
        launch.index+=1
        if launch.index>=launch.file_cnt:
            launch.index = 0
        print(launch.index)
        launch.draw_img(filelabel,launch.file_list[launch.index])
        gc.collect()
        print(gc.mem_free())
    elif key==0:
        print('OK')
        alarm.sleep_memory[0] = launch.index
        startApp='/app/'+ launch.file_list[launch.index]
        supervisor.set_next_code_file(startApp)
        print("\033[2J",end="") #clear screen
        print("Free memory:"+str(gc.mem_free()))
        print("Next boot set to:")
        print(startApp)
        try:
            gc.collect()
            exec(open(startApp).read())
        except Exception as err:
            print(err)
        print("Program finished ...")
        print("\033[2J",end="") #clear screen
        gc.collect()
        display.show(displaygroup)
        
        pass
        
 



