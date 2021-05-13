#
# fake_neopixel.py -- pure-python "fake" neopixel to test neopixel algorithms on computers
#
# https://github.com/todbot/circuitpython_ledtools
# 2021 - @todbot / Tod Kurt - 
#

import math

# Pixel color order constants
RGB = (0, 1, 2)
"""Red Green Blue"""
GRB = (1, 0, 2)
"""Green Red Blue"""
RGBW = (0, 1, 2, 3)
"""Red Green Blue White"""
GRBW = (1, 0, 2, 3)
"""Green Red Blue White"""

class NeoPixel:
    def __init__(self,pin,n,bpp=3,order=GRB,brightness=1.0,auto_write=True,pixel_order=None):
        self.pin = pin
        self.n = n
        self.bpp = bpp
        self.order = order
        self.buf1 = bytearray(n * bpp) # pre-brightness
        self.buf2 = bytearray(n * bpp) # post-brightness
        self.brightness = 1.0
        self.auto_write = auto_write
        if pixel_order is not None:
            self.order = pixel_order
        
    def show(self):
        #neopixel_write.neopixel_write(self.pin, self.buf2)
        print(f"{self.pin}:", end='')
        for i in range(0, self.n * self.bpp,3):
            print("#%02x%02x%02x " % (self.buf2[i+0],self.buf2[i+1],self.buf2[i+2]), end='')
        print()

    def fill(self,value):
        for i in range(self.n):
            self._set_item(i,value)
        if self.auto_write:
            self.show()
            
    def _set_item(self, index, value):
        if index < 0:
            index += len(self)
        if index >= self.n or index < 0:
            raise IndexError
        offset = index * self.bpp

        if isinstance(value, int):
            r = value >> 16
            g = (value >> 8) & 0xff
            b = value & 0xff
        else:
            r,g,b = value
        #print("\toffset:%d rgb:%x,%x,%x  %d/%d" %(offset,r,g,b, index,self.n))
        self.buf1[ offset + self.order[0] ] = r
        self.buf1[ offset + self.order[1] ] = g
        self.buf1[ offset + self.order[2] ] = b
        # apply brightness
        for i in range(self.n*self.bpp):
            self.buf2[i] = int(self.buf1[i] * self.brightness)
#            print("%s%02x" % (" " if i%3==0 else '',int(self.buf1[i] * self.brightness)), end='')
#        print()

    def __len__(self):
        return self.n

    def __getitem__(self, index): # array access
#        print("GETITEM",index)
        if isinstance(index, slice):
            print("SLICER")
            out = []
            for in_i in range(
                    *index.indices( len(self.buf2) // self.bpp)
            ):
                out.append(self._getitem(in_i))
            print("__getitem__:out:",out)
            return out
        if index < 0:
            index += len(self)
        if index >= self.n or index < 0:
            raise IndexError
        offset = index*self.bpp
        r = self.buf1[ offset + self.order[0] ]
        g = self.buf1[ offset + self.order[1] ] 
        b = self.buf1[ offset + self.order[2] ] 
        return (r,g,b)

    # stolen from https://github.com/adafruit/Adafruit_CircuitPython_Pypixelbuf/blob/master/adafruit_pypixelbuf.py
    # https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/blob/d426b0ca359cce706506fa709c1b107562787e4e/neopixel.py
    
    def __setitem__(self, index, val):   # array access
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self.buf1) // self.bpp)
            length = stop - start
            if step != 0:
                length = math.ceil(length / step)
            if len(val) != length:
                raise ValueError("Slice and input sequence size do not match.")
            for val_i, in_i in enumerate(range(start, stop, step)):
                self._set_item(in_i, val[val_i])
        else:
            self._set_item(index,val)
                
        if self.auto_write:
            self.show()
