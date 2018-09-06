#!/usr/bin/python

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# SPI ports on ADC
CLK = 18
MISO = 23
MOSI = 24
CS = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# SPI interface pins
GPIO.setup(MOSI, GPIO.OUT)
GPIO.setup(MISO, GPIO.IN)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)

# adc channels
pot_adc = 0;
ldr_adc = 1;

while True:
...

def readPot():

    val = mcp.read_adc(pot_adc)
    return (val/1024)*3.3 + " V"

def readLDR():

    val = mcp.read_adc(ldr_adc)
    return (val/1024)*100 + " %"
