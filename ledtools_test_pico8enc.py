
import time

import fake_neopixel as neopixel
#import neopixel

leds = neopixel.NeoPixel( 'fake', 8, order=neopixel.RGB, auto_write=False )

#
def color_blend(color1,color2,amount2):
    if isinstance(color1,int):
        (r1,g1,b1) = ((color1>>16) & 0xff),((color1>>8) & 0xff),((color1>>0) & 0xff)
    else:
        (r1,g1,b1) = color1
    if isinstance(color2,int):
        (r2,g2,b2) = ((color2>>16) & 0xff),((color2>>8) & 0xff),((color2>>0) & 0xff)
    else:
        (r2,g2,b2) = color2
    amount1 = 1.0 - amount2
    return (int(r1*amount1 + r2*amount2),
            int(g1*amount1 + g2*amount2),
            int(b1*amount1 + b2*amount2))

# convert midi cc value to a led strip info
def val_to_leds(color,val):
    n = len(leds)
    di = 128 // n    # change in i per value (128 values in midi CC)
    i = (val // di)
    p = (val/di) - i # percentage of light for next led
    leds.fill(color)
    leds[i] = color_blend(color,(255,255,255),1-p)
    if i!=n-1:
        leds[i+1] = color_blend(color,(255,255,255), p)
    leds.show()


val = 0
vinc = 1
while True:
#    val_to_leds((255,0,0), val)
    val_to_leds(0xee00ee, val)
    val = (val + vinc)
    if val<0 or val>127: vinc=-vinc; val +=vinc
    time.sleep(0.05)
