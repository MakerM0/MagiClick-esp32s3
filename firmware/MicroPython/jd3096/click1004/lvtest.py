import ili9XXX
import display
import lvgl as lv
import espidf as esp
import time
from machine import I2C, Pin


bl=Pin(37,Pin.OUT)
bl.on()
key=Pin(0,Pin.IN,Pin.PULL_UP)
btn=Pin(11,Pin.IN,Pin.PULL_UP)

disp = display.st7789(width=135, height=135,miso=1, mosi=4, clk=5, cs=9, dc=38, rst=10, mhz=80,backlight=37,spihost=esp.HSPI_HOST,rot=-3,invert=False)

lv.init()


def load_image(filename):
    filename=filename+'.png'
    with open(filename,'rb') as f:
        png_data = f.read()
    img=lv.img_dsc_t({
      'data_size': len(png_data),
      'data': png_data
    })
    return img

github = load_image('github')
csdn = load_image('cs')
lvgl = load_image('lvgl')

scr = lv.scr_act()
scr.set_style_bg_color(lv.color_hex(0xF0F0F0), lv.PART.MAIN)

style = lv.style_t()
style.init()
style.set_radius(15)

style.set_bg_opa(lv.OPA.COVER)
style.set_bg_color(lv.palette_main(lv.PALETTE.BLUE))
style.set_bg_grad_color(lv.palette_darken(lv.PALETTE.BLUE, 2))
#style.set_bg_grad_dir(lv.GRAD_DIR.VER)

style.set_border_opa(lv.OPA._40)
style.set_border_width(3)
style.set_border_color(lv.palette_main(lv.PALETTE.GREY))
# 
style.set_shadow_width(7)
style.set_shadow_color(lv.palette_main(lv.PALETTE.GREY))
style.set_shadow_ofs_y(7)

style.set_outline_opa(lv.OPA.COVER)
style.set_outline_color(lv.palette_main(lv.PALETTE.BLUE))

style.set_text_color(lv.color_white())
style.set_pad_all(10)

# Init the pressed style
style_pr = lv.style_t()
style_pr.init()

# Add a large outline when pressed
style_pr.set_outline_width(30)
style_pr.set_outline_opa(lv.OPA.TRANSP)

style_pr.set_translate_y(5)
style_pr.set_shadow_ofs_y(3)
style_pr.set_bg_color(lv.palette_darken(lv.PALETTE.BLUE, 2))
style_pr.set_bg_grad_color(lv.palette_darken(lv.PALETTE.BLUE, 4))

# Add a transition to the outline
trans = lv.style_transition_dsc_t()
props = [lv.STYLE.OUTLINE_WIDTH, lv.STYLE.OUTLINE_OPA, 0]
trans.init(props, lv.anim_t.path_linear, 300, 0, None)

style_pr.set_transition(trans)

btn1 = lv.btn(lv.scr_act())
btn1.remove_style_all()                          # Remove the style coming from the theme
btn1.add_style(style, 0)
btn1.add_style(style_pr, lv.STATE.PRESSED)
btn1.set_size(100, 100)
btn1.center()

btn_img = lv.img(btn1)
btn_img.set_src(lvgl)
btn_img.set_width(lv.SIZE_CONTENT)
btn_img.set_height(lv.SIZE_CONTENT) 
btn_img.set_y(-12)
btn_img.set_align( lv.ALIGN.CENTER)

btn_label = lv.label(btn1)
#btn_label.set_style_text_font(font1, 0)
btn_label.set_text('LVGL')
btn_label.set_width(lv.SIZE_CONTENT)
btn_label.set_height(lv.SIZE_CONTENT) 
btn_label.set_y(38)

btn_label.set_align(lv.ALIGN.CENTER)

 

def check_key(indev_drv, data):
    if btn.value()==0:
        data.point.x ,data.point.y = 64,64
        data.state = lv.INDEV_STATE.PRESSED
    else:
        data.state = lv.INDEV_STATE.RELEASED
        

indev_drv = lv.indev_drv_t()
indev_drv.init()
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = check_key
indev_drv.register()


f=0
while True:
    xv=key.value()
    if xv==0:
        if f==2:
            f=0
        else:
            f+=1
        time.sleep_ms(200)
    if f==0:
        btn_label.set_text('CSDN')
        btn_img.set_src(csdn)
    elif f==1:
        btn_label.set_text('GAYHUB')
        btn_img.set_src(github)
    elif f==2:
        btn_label.set_text('LVGL')
        btn_img.set_src(lvgl)


