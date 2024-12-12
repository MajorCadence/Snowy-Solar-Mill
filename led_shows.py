#import os # import os for system functions
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

small_sleep_time = 0.05
medium_sleep_time = 0.15
extra_long_sleep_time = 0.75

def LightShow1():
    while True:
        effect = rand.randint(9,9)
        colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
        if effect == 1:
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
        if effect == 2:
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
        if effect == 3:
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
        if effect == 4:
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
        if effect == 5:
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*ARM_COUNT + j, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time)
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*ARM_COUNT + j, Color(0, 0, 0))
                    strip.show()
                    sleep(small_sleep_time)
        if effect == 6:
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(LED_COUNT - 1 - (i*ARM_COUNT + (ARM_COUNT - j - 1)), Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time)
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(LED_COUNT - 1 - (i*ARM_COUNT + (ARM_COUNT - j - 1)), Color(0, 0, 0))
                    strip.show()
                    sleep(small_sleep_time)
        if effect == 7:
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(LED_COUNT -1 - (i*ARM_COUNT + j), Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time)
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(LED_COUNT -1 - (i*ARM_COUNT + j), Color(0, 0, 0))
                    strip.show()
                    sleep(small_sleep_time)
        if effect == 8:
            for i in range(4):
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*ARM_COUNT+ (ARM_COUNT - j - 1), Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time)
                for j in range(int(ARM_COUNT)):
                    strip.setPixelColor(i*ARM_COUNT+ (ARM_COUNT - j - 1), Color(0, 0, 0))
                    strip.show()
                    sleep(small_sleep_time)
        if effect == 9:
            for i in range(35):
                for j in range(LED_COUNT):
                    strip.setPixelColor(j, Color(colorR, colorG, colorB))
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                strip.show()
                sleep(medium_sleep_time)

def LightShow2():
    while True:
        effect = rand.randint(10,10)
        LEDs = [x for x in range(LED_COUNT)]
        rand.shuffle(LEDs)
        colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
        if effect == 1:
            for j in range(5):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(LED_COUNT):
                    strip.setPixelColor(LEDs[i], Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(0.05)
        if effect == 2:
            for j in range(5):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(LED_COUNT):
                    strip.setPixelColor(i, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(0.05)
        if effect == 3:
            for j in range(5):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(LED_COUNT):
                    strip.setPixelColor(LED_COUNT - 1 - i, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(0.05)
        if effect == 4:
            for j in range(5):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(LED_COUNT):
                    strip.setPixelColor(i, Color(colorR, colorG, colorB))
                    sleep(0.05)
                strip.show()
        if effect == 5:
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
        if effect == 6:
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
        if effect == 7:
            for k in range(10):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(4):
                    for j in range(i*ARM_COUNT, (i + 1) * ARM_COUNT):
                        strip.setPixelColor(j, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time*2)
                    for j in range(i*ARM_COUNT, (i + 1) * ARM_COUNT):
                        strip.setPixelColor(j, Color(0, 0, 0))
        if effect == 8:
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
        if effect == 9:
            for k in range(10):
                colorR, colorG, colorB = (round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1, round(254/2)*rand.randint(0,2) + 1)
                for i in range(4):
                    for j in range((3-i)*ARM_COUNT, (3 - i + 1) * ARM_COUNT):
                        strip.setPixelColor(j, Color(colorR, colorG, colorB))
                    strip.show()
                    sleep(small_sleep_time*2)
                    for j in range((3-i)*ARM_COUNT, (3 - i + 1) * ARM_COUNT):
                        strip.setPixelColor(j, Color(0, 0, 0))
        if effect == 10:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', action='store', help='Select the light show number to use')
    args = vars(parser.parse_args())
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    try:
        if args.get('number') == '1':
            LightShow1()
        elif args.get('number') == '2':
            LightShow2()
        elif args.get('number') == '3':
            pass
        elif args.get('number') == '4':
            pass
        else:
            print("Invalid light show specified (1-4)")
            exit(1)
    except KeyboardInterrupt:
        print("CTRL+C pressed")
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
        exit(1)