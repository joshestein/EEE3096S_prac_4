#!/usr/bin/python

import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import os

GPIO.setmode(GPIO.BCM)

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

reset_btn = 16
frequency_btn = 26

LDR_channel = 7
temp_sensor_channel = 0
pot_adc = 5

frequency = 0.5
state = off

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
GPIO.setup(reset_btn, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(frequency_btn, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(stop_btn, GPIO.IN, pull_up_down = GPIO.PUD.UP)

#callbacks
def callback_reset(channel):
    #clear screen
    if os.name == 'nt':
        #windows
        os.system('cls')
    else:
        os.system('clear')

    #TODO: reset timer (once timer function has been created)

def callback_frequency_change(channel):
    #need global to tell python about global var
    global frequency
    if frequency == 0.5:
        frequency = 1
    elif frequency == 1:
        frequency = 2
    else:
        frequency = 0.5

def callback_stop():
    if state == on:
        state == off
    else:
        state == on       

#interrupts
GPIO.add_event_detect(reset_btn, GPIO.FALLING, callback=callback_reset, bouncetime=200)
GPIO.add_event_detect(frequency_btn, GPIO.FALLING, callback=callback_frequency_change, bouncetime=200)
GPIO.add_event_detect(stop_btn, GPIO.FALLING, callback=callback_stop, bouncetime = 200)

mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)

def convert_voltage(data):
    #ldr needs to be proportioned to flashlight
    return round((data*3.3)/float(1023), 2)
    
def get_temp_in_degrees(temp_voltage):
    return (temp_voltage-500)/10

def get_ldr_percentage(ldr_voltage):
    #2.3 because there is a 1V drop across current limiting resistor
    percentage = 100*(1-ldr_voltage/2.35)
    if percentage > 0:
        return round(percentage, 2)
    else:
        return 0

def readPot():
    val = mcp.read_adc(pot_adc)
    return (val/1024)*3.3

while state == on:
    temp_level = mcp.read_adc(temp_sensor_channel)
    temp_voltage = convert_voltage(temp_level)
    temp = get_temp_in_degrees(temp_voltage)

    ldr_level = mcp.read_adc(LDR_channel)
    ldr_voltage = convert_voltage(ldr_level)
    ldr_percentage = get_ldr_percentage(ldr_voltage)

    print("{}, {} V, {} C".format(temp_level, temp_voltage, temp))
    #print("{} V, {}%".format(ldr_voltage, ldr_percentage))

    time.sleep(frequency)

