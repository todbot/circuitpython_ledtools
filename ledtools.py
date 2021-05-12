

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
            b = value & 0xf
        else:
            r,g,b = value
        return ( r,g,b )
    
    def make_fader_to_black(leds, by=1):
        return LEDAnimator(LEDTools.fade_to_black, leds, by)
    
    def make_blinker(leds, speed, color1, color2):
        return LEDAnimator(LEDTools.blink, leds, color1,color2)

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
        
