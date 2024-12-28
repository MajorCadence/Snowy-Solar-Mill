#import os # import os for system functions
import math
import sys
import argparse # argparse library for parsing command line arguments
from time import sleep # import sleep for delay
from rpi_ws281x import PixelStrip, Color # import the python ws281x library


LED_COUNT = 28 # 4 strands of 7 LEDs for a total of 28
LED_PIN = 21 # use GPIO pin 21 (PCM Dout)
LED_FREQ_HZ = 800000 # use a really high frequency for the LED PWM (this is default)
LED_DMA = 10 # the DMA channel to use for the LED memory (default - don't change this!)
LED_BRIGHTNESS = 64 # set the LED brightness to maximum (this is the starting value)
LED_INVERT = False # we are not using inverted signalling
LED_CHANNEL = 0 # default PWM channel - we are not using PWM; just leave this as-is
ARM_COUNT = round(LED_COUNT / 4)
import random as rand
rand.seed()

extra_small_sleep_time = 0.01
small_sleep_time = 0.05
medium_sleep_time = 0.15
extra_long_sleep_time = 0.75

def ClearLight():
    print("LightScript: Clearing all lights!!")
    for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()

def LightShow1():
    print("LightScript: Running light show 1!!")
    while True:
        effect = rand.randint(1,9)
        colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
        if effect == 1: #Clockwise, Radial Out
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*ARM_COUNT + j, Color(colorR, colorG, colorB))
                    sleep(small_sleep_time)
                    strip.show()
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*ARM_COUNT+ j, Color(0, 0, 0))
                    sleep(small_sleep_time)
                    strip.show()
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*ARM_COUNT + (ARM_COUNT - j - 1), Color(colorR, colorG, colorB))
                    sleep(small_sleep_time)
                    strip.show()
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*ARM_COUNT+ (ARM_COUNT - j - 1), Color(0, 0, 0))
                    sleep(small_sleep_time)
                    strip.show()
        if effect == 2: #Across, Radial Out
            for i in range(2):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*2*ARM_COUNT + j, Color(colorR, colorG, colorB))
                    sleep(small_sleep_time)
                    strip.show()
            for i in range(2):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*2*ARM_COUNT + j + ARM_COUNT, Color(colorR, colorG, colorB))
                    sleep(small_sleep_time)
                    strip.show()
            for i in range(2):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*2*ARM_COUNT + j, Color(0, 0, 0))
                    sleep(small_sleep_time)
                    strip.show()
            for i in range(2):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*2*ARM_COUNT + j + ARM_COUNT, Color(0, 0, 0))
                    sleep(small_sleep_time)
                    strip.show()
            for i in range(2):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*2*ARM_COUNT + (ARM_COUNT - j - 1), Color(colorR, colorG, colorB))
                    sleep(small_sleep_time)
                    strip.show()
            for i in range(2):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*2*ARM_COUNT + ARM_COUNT + (ARM_COUNT - j - 1), Color(colorR, colorG, colorB))
                    sleep(small_sleep_time)
                    strip.show()
            for i in range(2):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*2*ARM_COUNT + (ARM_COUNT - j - 1), Color(0, 0, 0))
                    sleep(small_sleep_time)
                    strip.show()
            for i in range(2):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*2*ARM_COUNT + ARM_COUNT + (ARM_COUNT - j - 1), Color(0, 0, 0))
                    sleep(small_sleep_time)
                    strip.show()
        if effect == 3: #Counterclockwise, Radial Out
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(LED_COUNT -1 - (i*ARM_COUNT + j), Color(colorR, colorG, colorB))
                    sleep(small_sleep_time)
                    strip.show()
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(LED_COUNT -1 - (i*ARM_COUNT+ j), Color(0, 0, 0))
                    sleep(small_sleep_time)
                    strip.show()
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(LED_COUNT - 1 - (i*ARM_COUNT + (ARM_COUNT - j - 1)), Color(colorR, colorG, colorB))
                    sleep(small_sleep_time)
                    strip.show()
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(LED_COUNT - 1 - (i*ARM_COUNT+ (ARM_COUNT - j - 1)), Color(0, 0, 0))
                    sleep(small_sleep_time)
                    strip.show()
        if effect == 4: #Snake
            for j in range(int(ARM_COUNT)):
                strip.setPixelColor(ARM_COUNT - 1 - j, Color(colorR, colorG, colorB))
                strip.show()
                sleep(small_sleep_time)
            for j in range(int(ARM_COUNT)):
                strip.setPixelColor(ARM_COUNT - 1 - j, Color(0, 0, 0))
                strip.setPixelColor(ARM_COUNT*2 + j, Color(colorR, colorG, colorB))
                strip.show()
                sleep(small_sleep_time)
            for j in range(int(ARM_COUNT)):
                strip.setPixelColor(ARM_COUNT*2 + j, Color(0, 0, 0))
                strip.show()
                sleep(small_sleep_time)
            for j in range(int(ARM_COUNT)):
                strip.setPixelColor(ARM_COUNT*2 - 1 - j, Color(colorR, colorG, colorB))
                strip.show()
                sleep(small_sleep_time)
            for j in range(int(ARM_COUNT)):
                strip.setPixelColor(ARM_COUNT*2 - 1 - j, Color(0, 0, 0))
                strip.setPixelColor(ARM_COUNT*3 + j, Color(colorR, colorG, colorB))
                strip.show()
                sleep(small_sleep_time)
            for j in range(int(ARM_COUNT)):
                strip.setPixelColor(ARM_COUNT*3 + j, Color(0, 0, 0))
                strip.show()
                sleep(small_sleep_time)
            for j in range(int(ARM_COUNT)):
                strip.setPixelColor(ARM_COUNT*4 - 1 - j, Color(colorR, colorG, colorB))
                strip.show()
                sleep(small_sleep_time)
            for j in range(int(ARM_COUNT)):
                strip.setPixelColor(ARM_COUNT*4 - 1 - j, Color(0, 0, 0))
                strip.setPixelColor(ARM_COUNT + j, Color(colorR, colorG, colorB))
                strip.show()
                sleep(small_sleep_time)
            for j in range(int(ARM_COUNT)):
                strip.setPixelColor(ARM_COUNT + j, Color(0, 0, 0))
                strip.show()
                sleep(small_sleep_time)
            for j in range(int(ARM_COUNT)):
                strip.setPixelColor(ARM_COUNT*3 - 1 - j, Color(colorR, colorG, colorB))
                strip.show()
                sleep(small_sleep_time)
            for j in range(int(ARM_COUNT)):
                strip.setPixelColor(ARM_COUNT*3 - 1 - j, Color(0, 0, 0))
                strip.setPixelColor(j, Color(colorR, colorG, colorB))
                strip.show()
                sleep(small_sleep_time)
            for j in range(int(ARM_COUNT)):
                strip.setPixelColor(j, Color(0, 0, 0))
                strip.show()
                sleep(small_sleep_time)
        if effect == 5: #Clockwise, Radial Out, One blade at a time
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*ARM_COUNT + j, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time)
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*ARM_COUNT + j, Color(0, 0, 0))
                    strip.show()
                    sleep(small_sleep_time)
        if effect == 6: #Counterclockwise, Radial Out, One blade at a time
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(LED_COUNT - 1 - (i*ARM_COUNT + (ARM_COUNT - j - 1)), Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time)
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(LED_COUNT - 1 - (i*ARM_COUNT + (ARM_COUNT - j - 1)), Color(0, 0, 0))
                    strip.show()
                    sleep(small_sleep_time)
        if effect == 7: #Counterclockwise, Radial In, One blade at a time
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(LED_COUNT -1 - (i*ARM_COUNT + j), Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time)
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(LED_COUNT -1 - (i*ARM_COUNT + j), Color(0, 0, 0))
                    strip.show()
                    sleep(small_sleep_time)
        if effect == 8: #Clockwise, Radial In, One blade at a time
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*ARM_COUNT+ (ARM_COUNT - j - 1), Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time)
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*ARM_COUNT+ (ARM_COUNT - j - 1), Color(0, 0, 0))
                    strip.show()
                    sleep(small_sleep_time)
        if effect == 9: #Rapid, Solid, Change, No Breaks
            for i in range(35):
                for j in range(LED_COUNT):
                    strip.setPixelColor(j, Color(colorR, colorG, colorB))
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                strip.show()
                sleep(medium_sleep_time)

def LightShow2():
    print("LightScript: Running light show 2!!")
    while True:
        effect = rand.randint(1,10)
        LEDs = [x for x in range(LED_COUNT)]
        rand.shuffle(LEDs)
        colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
        if effect == 1: #Dissolve Between
            for j in range(5):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(LED_COUNT):
                    strip.setPixelColor(LEDs[i], Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(0.05)
        if effect == 2: #Clockwise, Radial Out, Changing Between Colors
            for j in range(5):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(LED_COUNT):
                    strip.setPixelColor(i, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(0.05)
        if effect == 3: #Counterclockwise, Radial In, Changing Between Colors
            for j in range(5):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(LED_COUNT):
                    strip.setPixelColor(LED_COUNT - 1 - i, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(0.05)
        if effect == 4: #Slow, Solid, Change, No Breaks
            for j in range(5):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(LED_COUNT):
                    strip.setPixelColor(i, Color(colorR, colorG, colorB))
                    sleep(0.05)
                strip.show()
        if effect == 5: #Dissolve In/Out
            for j in range(3):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(LED_COUNT):
                    strip.setPixelColor(LEDs[i], Color(0, 0, 0))
                strip.show()
                for i in range(LED_COUNT):
                    strip.setPixelColor(LEDs[i], Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(0.05)
                strip.show()
                rand.shuffle(LEDs)
                for i in range(LED_COUNT):
                    strip.setPixelColor(LEDs[i], Color(0, 0, 0))
                    strip.show()
                    sleep(0.05)
        if effect == 6: #Clockwise, Blade Flashing
            for k in range(5):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(4):
                    for j in range(i*ARM_COUNT, (i + 1) * ARM_COUNT):
                        strip.setPixelColor(j, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(medium_sleep_time)
                    for j in range(i*ARM_COUNT, (i + 1) * ARM_COUNT):
                        strip.setPixelColor(j, Color(0, 0, 0))
                    strip.show()
                    sleep(medium_sleep_time)
        if effect == 7: #Clockwise, Fast Blade Flashing
            for k in range(10):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(4):
                    for j in range(i*ARM_COUNT, (i + 1) * ARM_COUNT):
                        strip.setPixelColor(j, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time*2)
                    for j in range(i*ARM_COUNT, (i + 1) * ARM_COUNT):
                        strip.setPixelColor(j, Color(0, 0, 0))
        if effect == 8: #Counterclockwise, Blade Flashing
            for k in range(5):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(4):
                    for j in range((3-i)*ARM_COUNT, (3 - i + 1) * ARM_COUNT):
                        strip.setPixelColor(j, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(medium_sleep_time)
                    for j in range((3-i)*ARM_COUNT, (3 - i + 1) * ARM_COUNT):
                        strip.setPixelColor(j, Color(0, 0, 0))
                    strip.show()
                    sleep(medium_sleep_time)
        if effect == 9: #Counterclockwise, Fast Blade Flashing
            for k in range(10):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(4):
                    for j in range((3-i)*ARM_COUNT, (3 - i + 1) * ARM_COUNT):
                        strip.setPixelColor(j, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time*2)
                    for j in range((3-i)*ARM_COUNT, (3 - i + 1) * ARM_COUNT):
                        strip.setPixelColor(j, Color(0, 0, 0))
        if effect == 10: #Slow, Solid, Change, Breaks
            for j in range(5):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(LED_COUNT):
                    strip.setPixelColor(i, Color(colorR, colorG, colorB))
                strip.show()
                sleep(extra_long_sleep_time)
                for i in range(LED_COUNT):
                    strip.setPixelColor(i, Color(0, 0, 0))
                strip.show()
                sleep(extra_long_sleep_time) 


def LightShow3():
    print("LightScript: Running light show 3!!")
    while True:
        effect = rand.randint(1,12)
        LEDs = [x for x in range(LED_COUNT)]
        rand.shuffle(LEDs)
        colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
        if effect == 1: #One led spiral out, back in, clockwise
            for _ in range(3):
                for i in range(ARM_COUNT):
                    for j in range(4):
                        strip.show()
                        strip.setPixelColor(i + j*7, Color(colorR, colorG, colorB))
                        strip.show()
                        sleep(small_sleep_time*1.5)
                        strip.setPixelColor(i + j*7, Color(0, 0, 0))
        if effect == 2: #One led spiral out, back in, counterclockwise
            for _ in range(3):
                for i in range(ARM_COUNT):
                    for j in range(4):
                        strip.show()
                        strip.setPixelColor(i + (3-j)*7, Color(colorR, colorG, colorB))
                        strip.show()
                        sleep(small_sleep_time*1.5)
                        strip.setPixelColor(i + (3-j)*7, Color(0, 0, 0))
        if effect == 3: #One led spiral out, earasing color, clockwise
            for _ in range(4):
                for led in range(LED_COUNT):
                    strip.setPixelColor(led, Color(colorR, colorG, colorB))
                strip.show()
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(ARM_COUNT):
                    for j in range(4):
                        strip.show()
                        strip.setPixelColor(i + j*7, Color(colorR, colorG, colorB))
                        strip.show()
                        sleep(small_sleep_time*2)
                        strip.setPixelColor(i + j*7, Color(0, 0, 0))
        if effect == 4: #One led spiral out, earasing color, counterclockwise
            for _ in range(4):
                for led in range(LED_COUNT):
                    strip.setPixelColor(led, Color(colorR, colorG, colorB))
                strip.show()
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(ARM_COUNT):
                    for j in range(4):
                        strip.show()
                        strip.setPixelColor(i + (3-j)*7, Color(colorR, colorG, colorB))
                        strip.show()
                        sleep(small_sleep_time*2)
                        strip.setPixelColor(i + (3-j)*7, Color(0, 0, 0))
        if effect == 5: #One led spiral out, adding color, clockwise
            for _ in range(4):
                for led in range(LED_COUNT):
                    strip.setPixelColor(led, Color(0, 0, 0))
                strip.show()
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                colorR2, colorG2, colorB2 = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(ARM_COUNT):
                    for j in range(4):
                        strip.show()
                        strip.setPixelColor(i + j*7, Color(colorR, colorG, colorB))
                        strip.show()
                        sleep(small_sleep_time*2)
                        strip.setPixelColor(i + j*7, Color(colorR2, colorG2, colorB2))
        if effect == 6: #One led spiral out, adding color, counterclockwise
            for _ in range(4):
                for led in range(LED_COUNT):
                    strip.setPixelColor(led, Color(0, 0, 0))
                strip.show()
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                colorR2, colorG2, colorB2 = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(ARM_COUNT):
                    for j in range(4):
                        strip.show()
                        strip.setPixelColor(i + (3-j)*7, Color(colorR, colorG, colorB))
                        strip.show()
                        sleep(small_sleep_time*2)
                        strip.setPixelColor(i + (3-j)*7, Color(colorR2, colorG2, colorB2))
        if effect == 7: #Two leds spiral out/in, clockwise then counterclockwise
            colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
            colorR2, colorG2, colorB2 = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
            for i in range(ARM_COUNT):
                for j in range(4):
                    strip.show()
                    strip.setPixelColor(i + j*7, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time*1)
                    strip.setPixelColor(i + j*7, Color(0, 0, 0))
                strip.show()
                sleep(small_sleep_time*2)
                for j in range(4):
                    strip.show()
                    strip.setPixelColor(6-i + j*7, Color(colorR2, colorG2, colorB2))
                    strip.show()
                    sleep(small_sleep_time*1)
                    strip.setPixelColor(6-i + j*7, Color(0, 0, 0))
                strip.show()
                sleep(small_sleep_time*2)
            colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
            colorR2, colorG2, colorB2 = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
            for i in range(ARM_COUNT):
                for j in range(4):
                    strip.show()
                    strip.setPixelColor(i + (3-j)*7, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time*1)
                    strip.setPixelColor(i + (3-j)*7, Color(0, 0, 0))
                strip.show()
                sleep(small_sleep_time*2)
                for j in range(4):
                    strip.show()
                    strip.setPixelColor(6-i + (3-j)*7, Color(colorR2, colorG2, colorB2))
                    strip.show()
                    sleep(small_sleep_time*1)
                    strip.setPixelColor(6-i + (3-j)*7, Color(0, 0, 0))
                strip.show()
                sleep(small_sleep_time*2)

        if effect == 8: #Two leds spiral out/in, counterclockwise
            colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
            colorR2, colorG2, colorB2 = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
            for i in range(ARM_COUNT):
                for j in range(4):
                    strip.show()
                    strip.setPixelColor(i + j*7, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time*1.5)
                    strip.setPixelColor(i + j*7, Color(0, 0, 0))
                strip.show()
                sleep(small_sleep_time*2)
                for j in range(4):
                    strip.show()
                    strip.setPixelColor(6-i + (3-j)*7, Color(colorR2, colorG2, colorB2))
                    strip.show()
                    sleep(small_sleep_time*1.5)
                    strip.setPixelColor(6-i + (3-j)*7, Color(0, 0, 0))
                strip.show()
                sleep(small_sleep_time*2)
            colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
            colorR2, colorG2, colorB2 = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
            for i in range(ARM_COUNT):
                for j in range(4):
                    strip.show()
                    strip.setPixelColor(i + (3-j)*7, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time*1.5)
                    strip.setPixelColor(i + (3-j)*7, Color(0, 0, 0))
                strip.show()
                sleep(small_sleep_time*2)
                for j in range(4):
                    strip.show()
                    strip.setPixelColor(6-i + j*7, Color(colorR2, colorG2, colorB2))
                    strip.show()
                    sleep(small_sleep_time*1.5)
                    strip.setPixelColor(6-i + j*7, Color(0, 0, 0))
                strip.show()
                sleep(small_sleep_time*2)

        if effect == 9: #Big, slow, multicolor snake spiral out
            for led in range(LED_COUNT):
                strip.setPixelColor(led, Color(0, 0, 0))
            strip.show()
            for i in range(ARM_COUNT):
                for j in range(4):
                    colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                    strip.show()
                    strip.setPixelColor(i + j*7, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(2*small_sleep_time + 3*small_sleep_time * (1 - abs(i-4.5)/4.5))
                    strip.setPixelColor(i-1 + j*7, Color(0, 0, 0))
        strip.setPixelColor(LED_COUNT - 1, Color(0, 0, 0))
        if effect == 10: #Big, slow, multicolor snake spiral in
            for led in range(LED_COUNT):
                strip.setPixelColor(led, Color(0, 0, 0))
            strip.show()
            for i in range(ARM_COUNT):
                for j in range(4):
                    colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                    strip.show()
                    strip.setPixelColor((6-i) + (3-j)*7, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(2*small_sleep_time + 2*small_sleep_time * (1 - abs(i-2.5)/2.5))
                    strip.setPixelColor((6-i)+1 + (3-j)*7, Color(0, 0, 0))
        strip.setPixelColor(0, Color(0, 0, 0))
        if effect == 11: #Whirlpool in
            for led in range(LED_COUNT):
                strip.setPixelColor(led, Color(0, 0, 0))
            strip.show()
            for i in range(15):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(ARM_COUNT):
                    for j in range(4):
                        strip.show()
                        strip.setPixelColor(i + j*7, Color(colorR, colorG, colorB))
                        strip.show()
                        sleep(extra_small_sleep_time*1.5)
            for i in range(ARM_COUNT):
                    for j in range(4):
                        strip.show()
                        strip.setPixelColor(i + j*7, Color(0, 0, 0))
                        strip.show()
                        sleep(extra_small_sleep_time*1.5)

        if effect == 12: #Whirlpool out
            for led in range(LED_COUNT):
                strip.setPixelColor(led, Color(0, 0, 0))
            strip.show()
            for i in range(15):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(ARM_COUNT):
                    for j in range(4):
                        strip.show()
                        strip.setPixelColor(6-i + (3-j)*7, Color(colorR, colorG, colorB))
                        strip.show()
                        sleep(extra_small_sleep_time*1.5)
            for i in range(ARM_COUNT):
                    for j in range(4):
                        strip.show()
                        strip.setPixelColor(6-i + (3-j)*7, Color(0, 0, 0))
                        strip.show()
                        sleep(extra_small_sleep_time*1.5)

def LightShow4():
    print("LightScript: Running light show 4!!")
    while True:
        effect = rand.randint(1,10)
        LEDs = [x for x in range(LED_COUNT)]
        rand.shuffle(LEDs)
        colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
        if effect == 1: #Rainbow fading
            for _ in range(2):
                for i in range(255):
                    for j in range(LED_COUNT):
                        strip.setPixelColor(j, Color(255-i, i, 0))
                    strip.show()
                    sleep(extra_small_sleep_time*1.5)
                for i in range(255):
                    for j in range(LED_COUNT):
                        strip.setPixelColor(j, Color(0, 255-i, i))
                    strip.show()
                    sleep(extra_small_sleep_time*1.5)
                for i in range(255):
                    for j in range(LED_COUNT):
                        strip.setPixelColor(j, Color(i, 0, 255-i))
                    strip.show()
                    sleep(extra_small_sleep_time*1.5)
        if effect == 2: #Rainbow fading faster
            for _ in range(5):
                for i in range(255):
                    for j in range(LED_COUNT):
                        strip.setPixelColor(j, Color(255-i, i, 0))
                    strip.show()
                    sleep(extra_small_sleep_time/4)
                for i in range(255):
                    for j in range(LED_COUNT):
                        strip.setPixelColor(j, Color(0, 255-i, i))
                    strip.show()
                    sleep(extra_small_sleep_time/4)
                for i in range(255):
                    for j in range(LED_COUNT):
                        strip.setPixelColor(j, Color(i, 0, 255-i))
                    strip.show()
                    sleep(extra_small_sleep_time/4)
        if effect == 3: #fading
            for _ in range(3):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(255):
                    for j in range(LED_COUNT):
                        strip.setPixelColor(j, Color(round(i*colorR/255), round(i*colorG/255), round(i*colorB/255)))
                    strip.show()
                    sleep(extra_small_sleep_time)
                for i in range(255):
                    for j in range(LED_COUNT):
                        strip.setPixelColor(j, Color(round((255-i)*colorR/255), round((255-i)*colorG/255), round((255-i)*colorB/255)))
                    strip.show()
                    sleep(extra_small_sleep_time)
        if effect == 4: #fading faster
            for _ in range(8):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(255):
                    for j in range(LED_COUNT):
                        strip.setPixelColor(j, Color(round(i*colorR/255), round(i*colorG/255), round(i*colorB/255)))
                    strip.show()
                    sleep(extra_small_sleep_time/8)
                for i in range(255):
                    for j in range(LED_COUNT):
                        strip.setPixelColor(j, Color(round((255-i)*colorR/255), round((255-i)*colorG/255), round((255-i)*colorB/255)))
                    strip.show()
                    sleep(extra_small_sleep_time/8)
        if effect == 5: #fading blades
            for _ in range(3):
                for k in range(4):
                    colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                    for i in range(255):
                        for j in range(7):
                            strip.setPixelColor(k*7 + j, Color(round(i*colorR/255), round(i*colorG/255), round(i*colorB/255)))
                        strip.show()
                        sleep(extra_small_sleep_time/4)
                    for i in range(255):
                        for j in range(7):
                            strip.setPixelColor(k*7 + j, Color(round((255-i)*colorR/255), round((255-i)*colorG/255), round((255-i)*colorB/255)))
                        strip.show()
                        sleep(extra_small_sleep_time/4)
        if effect == 6: #fading blades
            for _ in range(3):
                for k in range(4):
                    colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                    for i in range(255):
                        for j in range(7):
                            strip.setPixelColor((3-k)*7 + j, Color(round(i*colorR/255), round(i*colorG/255), round(i*colorB/255)))
                        strip.show()
                        sleep(extra_small_sleep_time/4)
                    for i in range(255):
                        for j in range(7):
                            strip.setPixelColor((3-k)*7 + j, Color(round((255-i)*colorR/255), round((255-i)*colorG/255), round((255-i)*colorB/255)))
                        strip.show()
                        sleep(extra_small_sleep_time/4)
        if effect == 7: #fading blades faster and together
            for _ in range(8):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for k in range(4):
                    for i in range(255):
                        for j in range(7):
                            strip.setPixelColor(k*7 + j, Color(round(i*colorR/255), round(i*colorG/255), round(i*colorB/255)))
                        strip.show()
                        sleep(extra_small_sleep_time/4)
                for k in range(4):
                    for i in range(255):
                        for j in range(7):
                            strip.setPixelColor(k*7 + j, Color(round((255-i)*colorR/255), round((255-i)*colorG/255), round((255-i)*colorB/255)))
                        strip.show()
                        sleep(extra_small_sleep_time/4)
        if effect == 8: #fading blades faster and together other way
            for _ in range(8):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for k in range(4):
                    for i in range(255):
                        for j in range(7):
                            strip.setPixelColor((3-k)*7 + j, Color(round(i*colorR/255), round(i*colorG/255), round(i*colorB/255)))
                        strip.show()
                        sleep(extra_small_sleep_time/4)
                for k in range(4):
                    for i in range(255):
                        for j in range(7):
                            strip.setPixelColor((3-k)*7 + j, Color(round((255-i)*colorR/255), round((255-i)*colorG/255), round((255-i)*colorB/255)))
                        strip.show()
                        sleep(extra_small_sleep_time/4)
        if effect == 9: #disco
                for k in range(255):
                    colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                    strip.setPixelColor(rand.randint(0, LED_COUNT), Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time)
        if effect == 10: #twinkling
                colorR, colorG, colorB = (round(254/4)*rand.randint(1,3), round(254/4)*rand.randint(1,3), round(254/4)*rand.randint(1,3))
                for p in range(LED_COUNT):
                    strip.setPixelColor(p, Color(colorR, colorG, colorB))
                strip.show()
                for k in range(20):
                    sleep(rand.randint(5, 20)/1000)
                    pixel = rand.randint(0, 27)
                    pixel2 = rand.randint(0, 27)
                    pixel3 = rand.randint(0, 27)
                    pixel4 = rand.randint(0, 27)
                    pixel5 = rand.randint(0, 27)
                    for p in range(40):
                       #colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                        strip.setPixelColor(pixel, Color(colorR + p, colorG + p, colorB + p))
                        strip.setPixelColor(pixel2, Color(colorR + p, colorG + p, colorB + p))
                        strip.setPixelColor(pixel3, Color(colorR + p, colorG + p, colorB + p))
                        strip.setPixelColor(pixel4, Color(colorR + p, colorG + p, colorB + p))
                        strip.setPixelColor(pixel5, Color(colorR + p, colorG + p, colorB + p))
                        strip.show()
                        sleep(extra_small_sleep_time/8)
                    for p in range(80):
                       #colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                        strip.setPixelColor(pixel, Color(colorR - p + 40, colorG - p + 40, colorB - p + 40))
                        strip.setPixelColor(pixel2, Color(colorR - p + 40, colorG - p + 40, colorB - p + 40))
                        strip.setPixelColor(pixel3, Color(colorR - p + 40, colorG - p + 40, colorB - p + 40))
                        strip.setPixelColor(pixel4, Color(colorR - p + 40, colorG - p + 40, colorB - p + 40))
                        strip.setPixelColor(pixel5, Color(colorR - p + 40, colorG - p + 40, colorB - p + 40))
                        strip.show()
                        sleep(extra_small_sleep_time/8)
                    for p in range(40):
                       #colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                        strip.setPixelColor(pixel, Color(colorR + p - 40, colorG + p - 40, colorB + p - 40))
                        strip.setPixelColor(pixel2, Color(colorR + p - 40, colorG + p - 40, colorB + p - 40))
                        strip.setPixelColor(pixel3, Color(colorR + p - 40, colorG + p - 40, colorB + p - 40))
                        strip.setPixelColor(pixel4, Color(colorR + p - 40, colorG + p - 40, colorB + p - 40))
                        strip.setPixelColor(pixel5, Color(colorR + p - 40, colorG + p - 40, colorB + p - 40))
                        strip.show()
                        sleep(extra_small_sleep_time/8)  


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', action='store', help='Select the light show number to use, 0 to clear')
    args = vars(parser.parse_args())
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    try:
        if args.get('number') == '0':
            ClearLight()
        elif args.get('number') == '1':
            LightShow1()
        elif args.get('number') == '2':
            LightShow2()
        elif args.get('number') == '3':
            LightShow3()
        elif args.get('number') == '4':
            LightShow4()
        else:
            print("Invalid light show specified (1-4)")
            exit(1)
    except KeyboardInterrupt:
        print("CTRL+C pressed")
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
        exit(1)