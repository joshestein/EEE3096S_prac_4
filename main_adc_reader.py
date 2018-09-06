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

LDR_channel = 7
temp_sensor_channel = 0
pot_adc = 5

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

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

while True:
    temp_level = mcp.read_adc(temp_sensor_channel)
    temp_voltage = convert_voltage(temp_level)
    temp = get_temp_in_degrees(temp_voltage)

    ldr_level = mcp.read_adc(LDR_channel)
    ldr_voltage = convert_voltage(ldr_level)
    ldr_percentage = get_ldr_percentage(ldr_voltage)

    #print("{}, {} V, {} C".format(temp_level, temp_voltage, temp))
    print("{} V, {}%".format(ldr_voltage, ldr_percentage))

    time.sleep(0.5)

