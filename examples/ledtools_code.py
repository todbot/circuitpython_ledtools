
import time
#import board
#from digitalio import DigitalInOut, Direction, Pull
#import neopixel
from fake_neopixel import NeoPixel
from ledtools import LEDTools as ledtools
import random

#import gc
#gc.collect()

num_leds = 16
led_pin = 'fake'
#led_pin = board.D2
#leds = neopixel.NeoPixel(led_pin, num_leds, brightness=0.2 )
#leds.fill((255,55,0))
#time.sleep(0.5)
leds = NeoPixel(led_pin, num_leds, brightness=0.2)
leds.fill(0xff00ff)

print("hello")

fade_by = ledtools.make_fader_to_black(leds, 5)

while True:
    #print(time.monotonic(),"hello",leds[0])
    ledtools.fade_to_black(leds, by=5)
    #fade_by.update()
    time.sleep(0.1)

tick=0
while True:
    #print(time.monotonic(),"hello",leds[0])
    #tricks.fade_to_black(leds, by=5)
    #fade1.animate()
    if tick % random.randint(5,10) == 0:
        leds[ random.randint(0,len(leds)-1) ] = (255,0,255)
    tick += 1
    time.sleep(0.01)
  
