#
#
# if running on commandline:
# PYTHONPATH=.. python3 ledtools_test.py

import time

import fake_neopixel as neopixel

from ledtools import LEDTools as ledtools

leds = neopixel.NeoPixel( 'fake', 10, order=neopixel.RGB, auto_write=False )

leds.fill( (0x11,0x22,0x33) )
leds[0] = (0x66,0x77,0x88)
leds[2] = (0xef,0xef,0xef)
leds.show()
print("leds[3]=",leds[3], ", leds len:",len(leds))

#leds[0:] = [(99,88,77) for l in leds]
#leds[0:] = [[max(i-5,0) for i in l] for l in leds]

h,s,v = (0,255,255)
r,g,b = ledtools.hsv2rgb(h,s,v)
print("hsv:%02x %02x %02x => rgb:%02x %02x %02x" % (h,s,v, r,g,b))


while True:
    #ledtools.fade_to_black(leds, by=5)
    ledtools.blink(leds, 0xefefef, 0x00ff00)
    #ledtools.blink(leds, (255,255,255), (0,255,0) )
    leds.show()
    time.sleep(0.1)

#leds.fill( 0xffffff )
#leds[0] = 0x333333
#xleds.show()


    
