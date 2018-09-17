#!/usr/bin/python

import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import os
import datetime

GPIO.setmode(GPIO.BCM)

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

reset_btn = 16
frequency_btn = 26
display_btn = 20
stop_btn = 21

LDR_channel = 7
temp_sensor_channel = 0
pot_channel = 5

frequency = 0.5
monitor = True
readings = []
#dummy date
prevTime = datetime.datetime(100,1,1,0,0,0)

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
GPIO.setup(reset_btn, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(frequency_btn, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(display_btn, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(stop_btn, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#callbacks
def callback_reset(channel):
    global prevTime, readings
    prevTime = datetime.datetime(100,1,1,0,0,0)
    readings = []
    #clear screen
    if os.name == 'nt':
        #windows
        os.system('cls')
    else:
        os.system('clear')

def callback_frequency_change(channel):
    global frequency
    if frequency == 0.5:
        frequency = 1
    elif frequency == 1:
        frequency = 2
    else:
        frequency = 0.5

def callback_display(channel):
    global readings
    for i in readings:
        print("{:10} | {} | {:10}V | {:10}C | {:10}%".format(i[0], i[1], i[2], i[3], i[4]))
    print("---------------------------------------------------------------------")

def callback_stop(channel):
    global monitor, readings
    if monitor == True:
        monitor = False
    else:
        monitor = True
        print("{:10} | {:8} | {:12} | {:10} | {:10}".format("Time", "Timer", "Pot", "Temp", "Light"))
        readings = []

#interrupts
GPIO.add_event_detect(reset_btn, GPIO.FALLING, callback=callback_reset, bouncetime=200)
GPIO.add_event_detect(frequency_btn, GPIO.FALLING, callback=callback_frequency_change, bouncetime=200)
GPIO.add_event_detect(display_btn, GPIO.FALLING, callback=callback_display, bouncetime=200)
GPIO.add_event_detect(stop_btn, GPIO.FALLING, callback=callback_stop, bouncetime=200)

mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)

def timer():
    global prevTime
    display = prevTime
    if frequency == 0.5:
	    newTime = prevTime + datetime.timedelta(0,5)
    elif frequency == 1:
	    newTime = prevTime + datetime.timedelta(0,10)
    else:
	    newTime = prevTime + datetime.timedelta(0,20)
    prevTime = newTime
    return display.time()

def convert_voltage(data):
    #ldr needs to be proportioned to flashlight
    return round((data*3.3)/float(1023), 2)
    
def get_temp_in_degrees(temp_voltage):
    temp = (temp_voltage+2.85-0.5)*10
    return round(temp,2)

def get_ldr_percentage(ldr_voltage):
    #2.3 because there is a 1V drop across current limiting resistor
    percentage = 100*(1-ldr_voltage/2.35)
    if percentage > 0:
        return round(percentage, 2)
    else:
        return 0

def get_pot_adjVoltage(pot_voltage):
    voltage = round(((pot_voltage-0.02)*3.3)/2.93, 2)
    if voltage > 3.3:
        return 3.3
    else:
        return voltage

print("{:10} | {:8} | {:12} | {:10} | {:10}".format("Time", "Timer", "Pot", "Temp", "Light"))
while True:
    if monitor == True:
        temp_level = mcp.read_adc(temp_sensor_channel)
        temp_voltage = convert_voltage(temp_level)
        temp = get_temp_in_degrees(temp_voltage)

        ldr_level = mcp.read_adc(LDR_channel)
        ldr_voltage = convert_voltage(ldr_level)
        ldr_percentage = get_ldr_percentage(ldr_voltage)

        pot_level = mcp.read_adc(pot_channel)
        pot_voltage = convert_voltage(pot_level)
        pot_adjVoltage = get_pot_adjVoltage(pot_voltage)

        #print("{}, {} V, {} C".format(temp_level, temp_voltage, temp))
        #print("{} V, {}%".format(ldr_voltage, ldr_percentage))
        #print("{} V".format(pot_adjVoltage))

        currentTime = time.strftime("%H:%M:%S")
        timer_now = timer()
        print("{:10} | {} | {:10}V | {:10}C | {:10}%".format(currentTime, timer_now, pot_adjVoltage, temp, ldr_percentage))
        print("----------------------------------------------------------------------")

        if len(readings) < 5:
            newReadings = [currentTime, timer_now, pot_adjVoltage, temp, ldr_percentage]
            readings.extend([newReadings])

        time.sleep(frequency)

