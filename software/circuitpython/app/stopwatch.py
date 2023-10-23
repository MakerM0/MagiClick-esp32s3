from magiclick import *

import time
import supervisor
from adafruit_simple_text_display import SimpleTextDisplay


from adafruit_display_text import label

display.show(None)
main_group = displayio.Group()

display.show(main_group)


# label
t_label = label.Label(terminalio.FONT,color = SimpleTextDisplay.GREEN,scale=2)
t_label.anchor_point = (0.5,0.0)
t_label.anchored_position = (display.width / 2, 0)
t_label.text='00:00:000'

main_group.append(t_label)

# label
order_labels=[]
order_color=[SimpleTextDisplay.GOLD ,
             SimpleTextDisplay.WHITE  ,
             SimpleTextDisplay.YELLOW ,
             SimpleTextDisplay.ORANGE  ,
             SimpleTextDisplay.YELLOW  ,
             SimpleTextDisplay.CYAN  ,
             SimpleTextDisplay.TEAL  ,
             SimpleTextDisplay.AQUA  ,
             SimpleTextDisplay.SKY    ,
             SimpleTextDisplay.VIOLET    ,
             SimpleTextDisplay.AMBER    ,
             SimpleTextDisplay.JADE    ,
             SimpleTextDisplay.PINK    ,
             SimpleTextDisplay.MAGENTA    ,
             ]

for j in range(2):
    for i in range(7):    
#         id_label = label.Label(terminalio.FONT,color = SimpleTextDisplay.order_color[i+j*7],scale=1)
        id_label = label.Label(terminalio.FONT,color = SimpleTextDisplay.JADE,scale=1)
        id_label.anchor_point = (0.0,0.0)
        id_label.anchored_position = ((display.width//2+10) *j, 25+i*15)    
        id_label.text='__:__:___'
        order_labels.append(id_label)
        main_group.append(id_label)

LEN = len(order_labels)


def ui_reset():
    t_label.color = SimpleTextDisplay.GREEN
    t_label.text="00:00:000"
    for i in range(LEN):
        order_labels[i].text="__:__:___"


class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.record_time = 0
        self.is_running = False
        self.is_paused = False

    def start(self):
        if not self.is_running:
            self.start_time = time.monotonic()
            self.is_running = True
            print("start")

    def pause(self):
        if self.is_running:
            self.elapsed_time += time.monotonic() - self.start_time
            self.is_running = False
            self.is_paused = True
            print("pause")

    def resume(self):
        if not self.is_running:
            self.start_time = time.monotonic()
            self.is_running = True
            self.is_paused = False
            print("resume")

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
        self.is_paused = False
        print("reset")

    def record(self):
        if self.is_running:
            self.current_time = time.monotonic() - self.start_time + self.elapsed_time
            print(f"Recorded: {self.current_time} s")

stopwatch = Stopwatch()

# display.show(None)
# 
# display.show(display.root_group)
# 
# display.root_group.scale = 1
# supervisor.reset_terminal(display.width,display.height)
# 
# print('       STOPWATCH   ')
# print(' \r\n'* 5)
cnt=0
while True:
    key = getkey()
    if key==0:
        if stopwatch.is_running:
            stopwatch.record()
            order_labels[cnt].text = "{:0>2d}:{:0>2d}:{:0>3d}".format(int(stopwatch.current_time//60),int(stopwatch.current_time//1%60),int(stopwatch.current_time*1000%1000))
            cnt+=1
            if cnt>=LEN:
                cnt=0
                ui_reset()
                stopwatch.reset()
                
        else:
            if stopwatch.is_paused == True:
                stopwatch.resume()
                stopwatch.record()
                t_label.color = SimpleTextDisplay.GREEN
                order_labels[cnt].text = "{:0>2d}:{:0>2d}:{:0>3d}".format(int(stopwatch.current_time//60),int(stopwatch.current_time//1%60),int(stopwatch.current_time*1000%1000))
                cnt+=1
                if cnt>=LEN:
                    cnt=0
                    ui_reset()
                    stopwatch.reset()
            else:
                stopwatch.start()
        
    if key==1:
        if stopwatch.is_running:
            stopwatch.pause()
            t_label.color = SimpleTextDisplay.RED
        else:
            stopwatch.resume()
            t_label.color = SimpleTextDisplay.GREEN
            
    if key==2:
        stopwatch.reset()
        ui_reset()
        cnt=0
    
    
    if stopwatch.is_running:
        x=time.monotonic() - stopwatch.start_time + stopwatch.elapsed_time
        t_label.text="{:0>2d}:{:0>2d}:{:0>3d}".format(int(x//60),int(x//1%60),int(x*1000%1000))
    
    acceleration = imu.acceleration
    if acceleration[2] > 8.0:
        returnMainPage()
    
    
    
        
        


