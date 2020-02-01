import time
import sys

wrt = sys.stdout.write

class Screen:
    BLOCK = '██'
    
    def __init__(self, width, height, offset=(0,0)):
        self.width = width
        self.height = height
        self.offset = offset

        self.data = [
            [(0,0,0, False) for _ in range(width)] for _ in range(height)
        ]

        wrt("\033[?47h")  # save current screen

    def close(self):
        wrt("\033[?47l")  # save current screen

    def __setitem__(self, coords, value):
        x, y = coords
        assert isinstance(value, tuple) and 3 <= len(value) <= 4
        r, g, b, *blink = value

        if len(blink) == 0 or blink[0] == False:
            blink= False
        else:
            blink = True

        assert (0<=r<=255) and (0<=g<=255) and (0<=b<=255)

        self.data[y][x] = (r, g, b, bool(blink))
    
    def line(self, x0, y0, x1, y1, color):
        """
        Bresenham's line algorithm
        @from: https://rosettacode.org/wiki/Bitmap/Bresenham%27s_line_algorithm#Python
        """
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1

        if dx > dy:
            err = dx / 2.0
            while x != x1:
                self[x, y] = color
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                self[x, y] = color
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy   

        self[x, y] = color

    def hline(self, x0, x1, y, color):
        if x1<0:
            x1+=self.width
        for x in range(x0, x1+1):
            self[x, y] = color

    def vline(self, x, y0, y1, color):
        if y1<0:
            y1+=self.height
        for y in range(y0, y1+1):
            self[x,y] = color
            
    def rect(self, x0, y0, x1, y1, color):
        """Draw rectangle"""
        if x1 < 0:
            x1 += self.width 
        if y1 < 0:
            y1 += self.height

        for x in range(x0, x1+1):
            self[x, y0] = self[x, y1] = color
        for y in range(y0, y1+1):
            self[x0, y] = self[x1, y] = color

    def fullrect(self, x0, y0, x1, y1, color):
        if x1 < 0:
            x1 += self.width 
        if y1 < 0:
            y1 += self.height

        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                self[x, y] = color

    def sync(self):
        wrt("\033[2J")  # clear entire screen
        for y in range(self.height):
            wrt("\033[%d;%dH" % (y+self.offset[1], 0 + 2 * self.offset[0]))  # move cursor to start of yth row
            for x in range(self.width):
                r, g, b, blink = self.data[y][x]

                if blink:
                    wrt(f"\033[5m\033[48;2;{r//4};{g//4};{b//4}m") # blinking color

                wrt(f"\033[38;2;{r};{g};{b}m%s\033[0m" % self.BLOCK)  # print block in given RGB color

            wrt('\n')
        wrt('\033[0m')  # reset all formating
    

