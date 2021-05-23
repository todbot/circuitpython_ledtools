#
# ledtools.py -- some tools to play with NeoPixels or similar on CircuitPython
#
# https://github.com/todbot/circuitpython_ledtools
# 2021 - @todbot / Tod Kurt - 
#

class LEDAnimator:
    def __init__(self,func, *args):
        self.func = func
        self.args = args
    
    def update(self):
        self.func(*self.args)
        #self.func(self.leds, self.args)
    
    
class LEDTools:

    def color_int_to_tuple(value):
        if isinstance(value, int):
            r = value >> 16
            g = (value >> 8) & 0xff
            b = value & 0xff
        else:
            r,g,b = value
        return ( r,g,b )
    
    def make_fader_to_black(leds, by=1):
        return LEDAnimator(LEDTools.fade_to_black, leds, by)
    
    def make_blinker(leds, speed, color1, color2):
        def update():
            LEDTools.blink(leds, color1,color2)
        return update

    def blink(leds, color1,color2):
        color1 = LEDTools.color_int_to_tuple(color1)
        color2 = LEDTools.color_int_to_tuple(color2)
        if leds[0] == color1:
            leds.fill(color2)
        else:
            leds.fill(color1)

    def fade_to_black(leds, by=1):
        leds[0:] = [[max(i-by,0) for i in l] for l in leds]

    def chaser(leds, speed, color, size, spacing):
        pass
    
    def blend(color1,color2,amount2):
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
    
    def shift(leds, amount, rotate=True):  # and rotate
        if a>0:
            t = leds[-amount:]
            leds[amount:] = leds[0:-amount]
            leds[0:amount] = t
        elif a<0:
            pass

    def rotate(leds, amount):
        if a>0:
            t = leds[-amount:]
            leds[amount:] = leds[0:-amount]
            leds[0:amount] = t
        elif a<0:
            pass
        
    def hsv2rgb(h, s, v):
        """ 
        Convert H,S,V in 0-255,0-255,0-255 format
        to R,G,B in 0-255,0-255,0-255 format
        (this is currently busted)
        """
        import math
        h = h/255
        s = s/255
        v = v/255
        h60 = h / 42.67
        h60f = math.floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0: r, g, b = v, t, p
        elif hi == 1: r, g, b = q, v, p
        elif hi == 2: r, g, b = p, v, t
        elif hi == 3: r, g, b = p, q, v
        elif hi == 4: r, g, b = t, p, v
        elif hi == 5: r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return r, g, b


    # stolen from     
    # https://github.com/wntrblm/Sol/blob/master/firmware/winterbloom_sol/_utils.py    
    def hsv_to_rgb(h, s, v):
        """ 
        Convert H,S,V in 0-255,0-255,0-255 format
        to R,G,B in 0-255,0-255,0-255 format
        """
        if s == 0: return v, v, v
        h = h/255
        s = s/255
        v = v/255
        i = int(h * 6.0)  # XXX assume int() truncates!
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        if i == 0: r = v; g = t; b = p
        if i == 1: r = q; g = v; b = p
        if i == 2: r = p; g = v; b = t
        if i == 3: r = p; g = q; b = v
        if i == 4: r = t; g = p; b = v
        if i == 5: r = v; g = p; b = q
        return int(r*255), int(g*255), int(b*255)
