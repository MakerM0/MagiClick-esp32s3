'''
v0.1.1
    20231008
    add 'quit action'


v0.1.0
    20231008
    
'''

from magiclick import *
import time
import board
import analogio


display.show(None)

TERMINAL_HEIGHT=display.height+20
display.root_group.scale = 1
    
display.root_group[0].hidden = False
display.root_group[1].hidden = True # logo
display.root_group[2].hidden = True # status bar
supervisor.reset_terminal(display.width,TERMINAL_HEIGHT)
display.root_group[0].y = 0

display.show(display.root_group)

analog_pin = analogio.AnalogIn(board.BAT)

def get_voltage(pin):
    return (pin.value * 3.3) / 65535 *2

get_voltage(analog_pin)
time.sleep(0.5)

now = 0
old = 0

while True:
    now =  time.monotonic()
    if (now-old) >= 2.0:
        print(f'{get_voltage(analog_pin)} V')         

    key = getkey() 
    if key==2 or key==1:
        print('exit')
        returnMainPage() 
    time.sleep(0.2)