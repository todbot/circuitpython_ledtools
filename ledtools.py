#
# ledtools.py -- some tools to play with NeoPixels or similar on CircuitPython
#
# https://github.com/todbot/circuitpython_ledtools
# 2021 - @todbot / Tod Kurt - 
#

# originally from     
# https://github.com/wntrblm/Sol/blob/master/firmware/winterbloom_sol/_utils.py
# and converted to 0-255 use
def hsv2rgb(h, s, v):
    """ 
    Convert H,S,V in 0-255,0-255,0-255 format
    to R,G,B in 0-255,0-255,0-255 format
    Converts an integer HSV (value range from 0 to 255) to an RGB tuple 
    """
    if s == 0: return v, v, v
    # Wrap values within range, scale to 0-1
    h = (h % 0xFF) / 255
    s = (s % 0xFF) / 255
    v = (v % 0xFF) / 255
    i = int(h * 6.0)  # XXX assume int() truncates!
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0: r,g,b = v,t,p
    if i == 1: r,g,b = q,v,p
    if i == 2: r,g,b = p,v,t
    if i == 3: r,g,b = p,q,v
    if i == 4: r,g,b = t,p,v
    if i == 5: r,g,b = v,p,q
    return int(r*255), int(g*255), int(b*255)

# originally from
# https://stackoverflow.com/questions/24152553/hsv-to-rgb-and-back-without-floating-point-math-in-python
# and modified slightly to 
def hsv2rgb_int(H,S,V):
    ''' 
    Convert H,S,V in 0-255,0-255,0-255 format
    to R,G,B in 0-255,0-255,0-255 format
    Uses only integer math. About 30% faster on M0. But less accurate
    '''
    # Check if the color is Grayscale
    if S == 0: return (V,V,V)
    # Wrap values within range
    H,S,V = H % 0xFF, S % 0xFF, V % 0xFF
    
    # Make hue 0-5 region
    region = H // 43;

    # Find remainder part, make it from 0-255
    remainder = (H - (region * 43)) * 6; 

    # Calculate temp vars, doing integer multiplication
    P = (V * (255 - S)) >> 8;
    Q = (V * (255 - ((S * remainder) >> 8))) >> 8;
    T = (V * (255 - ((S * (255 - remainder)) >> 8))) >> 8;

    # Assign temp vars based on color cone region
    if region == 0:   R,G,B = V,T,P
    elif region == 1: R,G,B = Q,V,P
    elif region == 2: R,G,B = P,V,T
    elif region == 3: R,G,B = P,Q,V
    elif region == 4: R,G,B = T,P,V
    else:             R,G,B = V,P,Q
    return (R, G, B)


def color_int_to_tuple(value):
    if isinstance(value, int):
        r = value >> 16
        g = (value >> 8) & 0xff
        b = value & 0xff
    else:
        r,g,b = value
    return ( r,g,b )

#def make_fader_to_black(leds, by=1):
#    return LEDAnimator(LEDTools.fade_to_black, leds, by)

def make_blinker(leds, speed, color1, color2):
    def update():
        blink(leds, color1,color2)
    return update

def blink(leds, colorA, colorB):
    cA = color_int_to_tuple(colorA)
    cB = color_int_to_tuple(colorB)
    c = leds[0]
    if c[0] == cA[0] and c[1] == cA[1] and c[2] == cA[2]:
        leds.fill(cB)
    else:
        leds.fill(cA)

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

    
