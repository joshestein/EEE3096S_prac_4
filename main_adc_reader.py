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

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)

def convert_voltage(data):
    #ldr needs to be proportioned to flashlight
    return (data*3.3)/float(1023)
    
def convert_temp(data):
    temp = ((data*330)/float(1023))-5

while True:
    #temp_level = mcp.read_adc(temp_sensor_channel)
    ldr_level = mcp.read_adc(LDR_channel)
    print("{} V".format(convert_voltage(ldr_level)))
    time.sleep(0.5)

