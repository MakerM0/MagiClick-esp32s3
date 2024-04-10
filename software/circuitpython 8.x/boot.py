import storage,usb_cdc
import board,digitalio
import microcontroller

button1 = digitalio.DigitalInOut(board.K1)
button1.pull = digitalio.Pull.UP

button3 = digitalio.DigitalInOut(board.K3)
button3.pull = digitalio.Pull.UP

# 禁止u盘出现
# if button1.value:
#     storage.disable_usb_drive()
    # 禁止cdc出现
#     usb_cdc.disable()



#进入uf2模式
# if button3.value:
#     microcontroller.on_next_reset(microcontroller.RunMode.UF2)
#     microcontroller.reset()

button1.deinit()    
button3.deinit()



