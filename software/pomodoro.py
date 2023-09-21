'''
pomodoro.py
v0.2.0
    20230725
    modify playwave
    
v0.1.0
    20230723
    first release
    
'''




from magiclick import *
from adafruit_display_text import label
import array
import math
import time
import audiocore
 
from adafruit_progressbar.horizontalprogressbar import (
    HorizontalProgressBar,
    HorizontalFillDirection,
)


WORK = 25
SHORTBREAK = 5
COLOR_STOPED = 0xff0000
COLOR_STARTED = 0x00ff00

# Generate one period of sine wav, 8ksps 440 Hz sin wave:
length = 8000 // 440
sine_wave = array.array("h", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * (2 ** 15))
sine_wave = audiocore.RawSample(sine_wave)

def playwave(filename):
    audiopwr_on()
    i2s = audiobusio.I2SOut(AUDIO_BCK,AUDIO_WS,AUDIO_DATA)
    try :
        wave_file = open('audio/pomodoro/{}'.format(filename), "rb")
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



# Define the Pomodoro class
class Pomodoro:
    def __init__(self,worktime:int,shortbreaktime:int):
        self.workmode=0
        self.shortbreakmode=1
        
        self.worktime = worktime
        self.shortbreaktime = shortbreaktime
        
        self.time=self.worktime
        self.mode= self.workmode
        self.minutes = self.worktime
        self.seconds = 0
        self.is_running = False

    def display_time(self):
        # Calculate the remaining time in minutes and seconds
        remaining_minutes = self.minutes
        remaining_seconds = self.seconds

        # Display the remaining time
        print(f"Time remaining: {remaining_minutes:02d}:{remaining_seconds:02d}")
    def setmode(self,mode):
        if mode==self.workmode:            
            self.time = self.worktime
        elif mode==self.shortbreakmode:
            self.time = self.shortbreaktime
        self.mode = mode
        
        
    def getmode(self):
        return self.mode
        
        
    def reset(self):
        # Reset the timer to the default values
        self.minutes = self.time 
        self.seconds = 0
        self.is_running = False

    def start(self):
        # Start the timer
        self.is_running = True

    def pause(self):
        # Pause the timer
        self.is_running = False

    def toggle(self):
        # Toggle the timer between running and paused
        self.is_running = not self.is_running
        

# Create an instance of the Pomodoro class
pomodoro = Pomodoro(WORK,SHORTBREAK)


display.show(None)
main_group = displayio.Group()

# label
t_label = label.Label(terminalio.FONT, color=COLOR_STARTED, scale=4)
t_label.anchor_point = (0.5, 0.0)
t_label.anchored_position = (display.width / 2, 40)
t_label.text = f"{WORK:02d}:{00:02d}"

mode_label = label.Label(terminalio.FONT, color=0xB4D7FA, scale=2)
mode_label.anchor_point = (0.5, 0.0)
mode_label.anchored_position = (display.width / 2, 10)
mode_label.text = "Pomodoro" 

main_group.append(t_label)
main_group.append(mode_label) 


# set progress bar width and height relative to board's display
width = display.width - 10
height = 15

x = display.width // 2 - width // 2
y = display.height // 2+30

# Create a new progress_bar object at (x, y)
progress_bar = HorizontalProgressBar(
    (x, y), (width, height), direction=HorizontalFillDirection.LEFT_TO_RIGHT
)

# Append progress_bar to the splash group
main_group.append(progress_bar)
display.show(main_group)
playwave('go.wav')

t_old=0
# Main loop to update and display the timer
while True:
    if (time.monotonic()-t_old) >= 1.0:
        t_old = time.monotonic()
        if pomodoro.is_running:
        # Decrease the timer by 1 second
            if pomodoro.seconds > 0:
                pomodoro.seconds -= 1
            elif pomodoro.minutes > 0:
                pomodoro.minutes -= 1
                pomodoro.seconds = 59
            else:
                mode = pomodoro.getmode()
                if mode==pomodoro.workmode:
                    pomodoro.setmode(pomodoro.shortbreakmode)
                    mode_label.text = "Break" 
                    t_label.color = COLOR_STOPED
                elif mode==pomodoro.shortbreakmode:
                    pomodoro.setmode(pomodoro.workmode)
                    mode_label.text = "Pomodoro" 
                    t_label.color = COLOR_STOPED
                # Timer has reached 0, reset the timer
                pomodoro.reset()
                mode = pomodoro.getmode()
                if mode == pomodoro.workmode:
                    playwave('go.wav')
                elif mode==pomodoro.shortbreakmode:
                    playwave('break.wav')
            # Display the timer
            pomodoro.display_time()
            t_label.text = f"{pomodoro.minutes:02d}:{pomodoro.seconds:02d}"
            progress_bar.value = int((1- ((pomodoro.minutes*60+pomodoro.seconds)/(pomodoro.time*60) ))*(progress_bar.maximum - progress_bar.minimum))
    

    
    key = getkey()
    if key==0:
        if not pomodoro.is_running:
            t_label.color = COLOR_STARTED
            pomodoro.start()
            t_old = time.monotonic()
        else:
            t_label.color = COLOR_STOPED
            pomodoro.pause()
    if key==2  :
         
        mode = pomodoro.getmode()
        if mode==pomodoro.workmode:
            pomodoro.setmode(pomodoro.shortbreakmode)
            mode_label.text = "Break" 
        elif mode==pomodoro.shortbreakmode:
            pomodoro.setmode(pomodoro.workmode)
            mode_label.text = "Pomodoro" 
        pomodoro.reset()
        t_label.color = COLOR_STARTED
        t_label.text = f"{pomodoro.minutes:02d}:{pomodoro.seconds:02d}"
        progress_bar.value = progress_bar.minimum
            
                
            
    # Wait for 1 second
    time.sleep(0.1)
    
    acceleration = imu.acceleration
    if acceleration[2] > 8.0:        
        returnMainPage()
    
    




