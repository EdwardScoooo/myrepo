# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries

# SPDX-License-Identifier: MIT


"""

Example sketch to connect to PM2.5 sensor with either I2C or UART.

"""


# pylint: disable=unused-import

import time

import board

import busio

from digitalio import DigitalInOut, Direction, Pull

from adafruit_pm25.i2c import PM25_I2C

import csv
import os



reset_pin = None

# If you have a GPIO, its not a bad idea to connect it to the RESET pin

# reset_pin = DigitalInOut(board.G0)

# reset_pin.direction = Direction.OUTPUT

# reset_pin.value = False



# For use with a computer running Windows:

# import serial

# uart = serial.Serial("COM30", baudrate=9600, timeout=1)


# For use with microcontroller board:

# (Connect the sensor TX pin to the board/computer RX pin)

# uart = busio.UART(board.TX, board.RX, baudrate=9600)


# For use with Raspberry Pi/Linux:

# import serial

# uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)


# For use with USB-to-serial cable:

# import serial

# uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0.25)


# Connect to a PM2.5 sensor over UART

# from adafruit_pm25.uart import PM25_UART

# pm25 = PM25_UART(uart, reset_pin)


# Create library object, use 'slow' 100KHz frequency!

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Connect to a PM2.5 sensor over I2C

pm25 = PM25_I2C(i2c, reset_pin)





sOut03=0
sOut05=0
sOut10=0
sOut25=0
sOut50=0
sOut100=0

sOut10env=0
sOut25env=0
sOut100env=0




print("Found PM2.5 sensor, reading data...")





while True:

    time.sleep(1)


    try:

        aqdata = pm25.read()

        #print(aqdata)

    except RuntimeError:

        print("Unable to read from sensor, retrying...")

        continue



##here the program starts to print out the value of the particualtes

    #print()

    print("Concentration Units (standard)")

    print("---------------------------------------")

    print(

        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"

        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])

    )

        
    print("Concentration Units (environmental)")

    print("---------------------------------------")

    print(

        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"

        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])

    )

    print("---------------------------------------")

    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])

    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])

    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])

    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])

    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])

    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])

    print("---------------------------------------")

    print('DSP filter')
    


    sampI03=aqdata['particles 03um']
    print('Sample In 03um:',sampI03)
    sampI03=sampI03*.1

    sOut03=round(sampI03+sOut03*.9,2)
    print("Sample out 03um:",sOut03)

    sampI03= sampI03/.1
    alert03=sampI03-sOut03
        


    sampI05=aqdata['particles 05um']
    print('Sample In 05um:',sampI05)
    sampI05=sampI05*.1

    sOut05=round(sampI05+sOut05*.9,2)
    print("Sample out 05um:",sOut05)

    alert05=sampI05-sOut05
    

    sampI10=aqdata['particles 10um']
    print('Sample In 10um:',sampI10)
    sampI10=sampI10*.1

    sOut10=round(sampI10+sOut10*.9,2)
    print("Sample out 10um:",sOut10)

    alert10=sampI10-sOut10
    
    sampI25=aqdata['particles 25um']
    print('Sample In 25um:',sampI25)
    sampI05=sampI05*.1

    sOut25=round(sampI25+sOut25*.9,2)
    print("Sample out 25um:",sOut25)

    alert25=sampI25-sOut25
    
    sampI50=aqdata['particles 50um']
    print('Sample In 50um:',sampI50)
    sampI50=sampI50*.1

    sOut50=round(sampI50+sOut50*.9,2)
    print("Sample out 50um:",sOut50)

    alert50=sampI50-sOut50
    
    sampI100=aqdata['particles 100um']
    print('Sample In 100um:',sampI100)
    sampI100=sampI100*.1

    sOut100=round(sampI100+sOut100*.9,2)
    print("Sample out 05um:",sOut100)

    alert100=sampI100-sOut100
    
    

    sampI10env=aqdata['pm10 env']
    print('Sample In pm10 Env:',sampI10env)
    sampI10env=sampI10env*.1

    sOut10env=round(sampI10env+sOut10env*.9,2)
    print("Sample out pm10 Env:",sOut10env)

    alert10env=sampI03-sOut03
    
    sampI25env=aqdata['pm25 env']
    print('Sample In pm2.5 Env:',sampI25env)
    sampI25env=sampI25env*.1

    sOut25env=round(sampI25env+sOut25env*.9,2)
    print("Sample out pm2.5 Env:",sOut25env)

    alert25env=sampI25env-sOut25env
    
    sampI100env=aqdata['pm100 env']
    print('Sample In pm100 Env:',sampI100env)
    sampI100env=sampI100env*.1

    sOut100env=round(sampI100env+sOut100env*.9,2)
    print("Sample out pm10 Env:",sOut100env)
    alert100env=sampI100env-sOut100env


    if alert03>100:
        print("================================")
        print('03um Particles are Increasing')
        print("================================")
    elif alert03<-100:
        print("================================")
        print('03um Particles are Decreasing')
        print("================================")
    
    if alert05>100:
        print("================================")
        print('05um Particles are Increasing')
        print("================================")
    elif alert05<-100:
        print("================================")
        print('05um Particles are Decreasing')
        print("================================")
    
    if alert10>100:
        print("================================")
        print('10um Particles are Increasing')
        print("================================")
    elif alert10<-100:
        print("================================")
        print('10um Particles are Decreasing')
        print("================================")

    if alert25>100:
        print("================================")
        print('25um Particles are Increasing')
        print("================================")
    elif alert25<-100:
        print("================================")
        print('25um Particles are Decreasing')
        print("================================")

    if alert50>100:
        print("================================")
        print('50um Particles are Increasing')
        print("================================")
    elif alert50<-100:
        print("================================")
        print('50um Particles are Decreasing')
        print("================================")

    if alert100>100:
        print("================================")
        print('100um Particles are Increasing')
        print("================================")
    if alert100<-100:
        print("================================")
        print('100um Particles are Decreasing')
        print("================================")



    if alert10env>100:
        print("================================")
        print('PM 1.0 Enviormental Particles are Increasing')
        print("================================")
    elif alert10env<-100:
        print("================================")
        print('PM 1.0 Enviormental Particles are Decreasing')
        print("================================")

    if alert25env>100:
        print("================================")
        print('PM 2.5 Enviormental um Particles are Increasing')
        print("================================")
    elif alert25env<-100:
        print("================================")
        print('PM 2.5 Enviormental Particles are Decreasing')
        print("================================")


    if alert100env>100:
        print("================================")
        print('PM 10.0 Enviormental um Particles are Increasing')
        print("================================")
    elif alert100env<-100:
        print("================================")
        print('PM 10.0 Enviormental Particles are Decreasing')
        print("================================")
    







    







    
