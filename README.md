
<p align="center">
    <br>
    <img src="https://avatars.githubusercontent.com/u/117961102" width="150"/>
    <br>
</p>
<p align="center">   
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/MakerM0/MagiClick-esp32s3">
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/MakerM0/MagiClick-esp32s3">  
</p>


https://github.com/user-attachments/assets/02206fc1-4ecb-459a-b24e-a9fd3fc22468

# MagiClick S3

<a href="https://www.pcbway.com/project/shareproject/MagiClick_S3_Single_506b8396.html"><img src="https://www.pcbway.com/project/img/images/frompcbway-1220.png" alt="PCB from PCBWay" /></a>



## Supported modules & chips

- ESP32-S3-MINI-1-N4R2  (for  Hardware v2.0)
- ESP32-S3-MINI-1-N8 (for  Hardware v2.0)
- ESP32-S3FN8  (for  Hardware v2.3)






# Purchase

[you can conveniently purchase it from here](https://www.elecrow.com/magiclick-open-source-multifunctional-programmable-mechanical.html).



| HW 2.0                       | [HW 2.3b ](hardware)             | [HW 2.3c](hardware)          |
| ---------------------------- | -------------------------------- | ---------------------------- |
| ![1](documents/images/1.jpg) | ![19](documents/images/19_1.png) | ![7](documents/images/7.png) |





# Specifications

A single-button keyboard, based on ESP32-S3, with a color screen.

CircuitPython is used by default. You can also use MicroPython, Arduino.

- 0.85-inch color screen, 128x128 resolution
- esp32-s3, which supports WiFi, flash and RAM large enough to help add more functional scripts
- The overall operation is mainly based on the mechanical axis buttons in the middle, and the left and right sides of the fuselage are generally used as auxiliaries
- The keyboard axis uses a pluggable design, and you can freely choose the silent axis or others
- Built-in a small speaker, listening to a sound is so easy
- An on-board 6-axis motion sensor
- There is an expansion port on the rear side of the fuselage
- USB Type-C interface
- One reset button at the bottom
- On-board colorful LEDs



# Hardware 

### v2.3

![20240819_164759](https://github.com/user-attachments/assets/72df055e-1152-4552-a693-6c6f89c9b059)



### Difference between v2.0 and v2.3

|                                          |                             v2.0                             |                             v2.3                             |
| ---------------------------------------- | :----------------------------------------------------------: | :----------------------------------------------------------: |
| Display Driver                           |                            GC9107                            |                            NV3023                            |
|                                          | <img src="https://github.com/user-attachments/assets/523d0a3c-ad5c-45c5-bae5-af37dbe8f4df" alt="GC9107" height=150 /> | <img src="https://github.com/user-attachments/assets/cd7b9db4-63ff-4de5-b79d-df9c267f4ca3" alt="NV3023" height=150 /> |
| Battery(with a protection circuit board) |                            801230                            |                       602025 or 802025                       |
|                                          | <img src="https://github.com/user-attachments/assets/7210dbef-53c5-4370-846a-e92d67251280" alt="18" height=150 /> |                                                              |
| Keyboard switch                          | <img src="https://github.com/user-attachments/assets/591edf82-1dd9-41aa-b90f-4f15ff3cf00b" alt="16-09-2024 13 45 53" height=150/> | <img src="https://github.com/user-attachments/assets/6c8d2646-7472-4314-a1af-7253ca38c896" alt="16-09-2024 13 45 38" height=150 /> |
|                                          |                                                              |                                                              |



# Software

Supports development using Arduino, CircuitPython, and MicroPython.



The "software" and "firmware" folders in this repository primarily contains the source code related to the hardware version 2.0. 

When you update the circuitpython firmware of the 2.0 hardware to version 9.x, the contents of the 2.3 software [here](https://github.com/MakerM0/MagiClick-S3-Single) folder can then be used by the 2.0 hardware.



For version 2.3, please click  [here](https://github.com/MakerM0/MagiClick-S3-Single).

### Guide

1. Use the Flash Download Tool to burn the Combined .bin in the Firmware folder to the board
2. After rebooting, Then copy the **.uf2** file to a USB stick
3. After rebooting, copy the contents of the softerware folder to the displayed USB stick

 [help](documents/如何下载固件.pdf) 


##### Settings.toml 

modify your wifi information, know the weather key (need to go to the official website to apply) and city

The main button is used to access the function options

The side button or flip button can exit the current function and return to the home page

##### How to add new features

Add the .py file to the app folder



# Mechanical

#### 3D Printings

[The latest files for PCB  version 2.0](https://makerworld.com/zh/models/404976#profileId-306794)

[The latest files for PCB  version 2.3](https://makerworld.com/zh/models/440612#profileId-346290)

[The latest files for PCB  version 2.3](https://makerworld.com/zh/models/584488#profileId-505582)

[PACKAGING BOX](https://makeronline.com/en/model/product%20packaging%20box/48433.html)

<img src="documents/images/172822164043371300-670291c869e3_thumbnail.jpg" alt="172822164043371300-670291c869e3_thumbnail"   width = 600/>



## How to contribute

Please use PR to submit contributions

In the **thirdparty** folder, create a project folder according to your own content, the naming needs to be intuitive and easy to understand, and the open source license should be added according to your own wishes

Please add a summary of the contributions in the file **contributer.md**, Add it at the end



## Images

| ![4](documents/images/11.jpg)                                | ![5](documents/images/15.jpg)                                | ![6](documents/images/12.jpg)                                |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![9](documents/images/16.jpg)                                | <img src="extention/MLX90640/images/5.jpg" alt="5" style="zoom:80%;" /> | ![20240929_153110_mini](documents/images/20240929_153110_mini.jpg) |
| ![7](documents/images/13.jpg)                                | ![8](documents/images/14.jpg)                                | <img src="extention/MLX90640/images/6.jpg" alt="6" style="zoom: 80%;" /> |
| ![172822164043371300-670291c869e3_thumbnail](documents/images/172822164043371300-670291c869e3_thumbnail.jpg) |                                                              |                                                              |
|                                                              |                                                              |                                                              |





# Extra

The most icons is from https://icons8.com/.

Other resource files come from the internet. 

If there are copyright issues involved, please contact me to delete them.



# License

(documents/hardware/mechanical)[Creative Commons — Attribution-NonCommercial-ShareAlike 4.0 International — CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

