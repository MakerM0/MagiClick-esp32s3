
<p align="center">
    <br>
    <img src="https://avatars.githubusercontent.com/u/117961102" width="150"/>
    <br>
</p>
<p align="center">   
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/MakerM0/MagiClick-esp32s3">
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/MakerM0/MagiClick-esp32s3">  
</p>


# [MagiClick S3](https://oshwhub.com/kakaka/lao-ban-jian-yi-wei-ke-bian-chen)
[afdian.net](https://afdian.net/a/modular)     |     [bilibili](https://space.bilibili.com/204526879)    |    [Circuitpython](https://circuitpython.org/board/magiclick_s3/)     |    [OSHWHUB](https://oshwhub.com/kakaka/lao-ban-jian-yi-wei-ke-bian-chen)



## Supported modules

- ESP32-S3-MINI-1-N4R2
- ESP32-S3-MINI-1-N8



## Specifications

A single-button keyboard, based on ESP32-S3, with a color screen.

CircuitPython is used by default. You can also use MicroPython, Arduino.

- 0.85-inch color screen, 128x128 resolution
-  esp32-s3, which supports WiFi, flash and RAM large enough to help add more functional scripts
- The overall operation is mainly based on the mechanical axis buttons in the middle, and the left and right sides of the fuselage are generally used as auxiliaries
- The keyboard axis uses a pluggable design, and you can freely choose the silent axis or others
- Built-in a small speaker, listening to a sound is so easy
- An on-board 6-axis motion sensor
- There is an expansion port on the rear side of the fuselage
- USB Type-C interface
- One reset button at the bottom
- On-board colorful LEDs

![1](documents/images/1.jpg)



## Guide

1. Use the Flash Download Tool to burn the Combined .bin in the Firmware folder to the board
2. After rebooting, Then copy the **.uf2** file to a USB stick
3. After rebooting, copy the contents of the softerware folder to the displayed USB stick

 [如何下载固件.pdf](documents/如何下载固件.pdf) 


#### Settings.toml 

modify your wifi information, know the weather key (need to go to the official website to apply) and city

The main button is used to access the function options

The side button or flip button can exit the current function and return to the home page





## How to add new features

Add the .py file to the app folder



## How to add a contribution

Please use PR to submit contributions

In the **thirdparty** folder, create a project folder according to your own content, the naming needs to be intuitive and easy to understand, and the open source license should be added according to your own wishes

Please add a summary of the contributions in the file **contributer.md**, Add it at the end

请使用pr提交贡献内容

在**第三方**文件夹内，根据自己的内容创建一个项目文件夹，命名需要直观易懂，开源协议请根据自我意愿添加

请添加所贡献的内容概要在文件contributer.md，在结尾添加即可



## Images

![4](documents/images/11.jpg)

![5](documents/images/15.jpg)

![6](documents/images/12.jpg)

![7](documents/images/13.jpg)

![8](documents/images/14.jpg)

![9](documents/images/16.jpg)

![10](documents/images/17.jpg)

<img src="extention/MLX90640/images/6.jpg" alt="6" style="zoom: 80%;" />

<img src="extention/MLX90640/images/5.jpg" alt="5" style="zoom:80%;" />



## Mechanical

![2](documents/images/2.gif)

![3](documents/images/3.gif)

## License

(documents/hardware/mechanical)[Creative Commons — Attribution-NonCommercial-ShareAlike 4.0 International — CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)



## About the Battery

Users can choose the **801230** battery with protection board.

However, choose a battery with safety certification.

Users need to control their own risks.

In the case of non-optimization, the battery will last at least 3 hours and the charging current is currently limited to 100mA.

The battery needs to be soldered to a board containing the MCU.

![08-10-2023 19.32.42](documents/images/08-10-2023 19.32.42.jpg)







## Extra

The most icons is from https://icons8.com/.

Other resource files come from the internet. 

If there are copyright issues involved, please contact me to delete them.
