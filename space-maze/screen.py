import time
import sys

wrt = sys.stdout.write

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.data = [
            [(0,0,0) for _ in range(width)] for _ in range(height)
        ]

        wrt("\033[?47h")  # save current screen

    def __del__(self):
        wrt("\033[?47l")  # save current screen

    def __setitem__(self, coords, value):
        x, y = coords
        assert isinstance(value, tuple) and len(value) == 3
        r, g, b = value
        assert (0<=r<=255) and (0<=g<=255) and (0<=b<=255)

        self.data[y][x] = (r, g, b)

    def sync(self):
        wrt("\033[2J")  # clear entire screen
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.data[y][x]
                wrt(f"\033[38;2;{r};{g};{b}m")
                wrt('██')
            wrt('\n')
        wrt('\033[0m')  # reset all formating
    


if __name__ == '__main__':

    WIDTH, HEIGHT = 84, 48
    scr = Screen(width=WIDTH, height=HEIGHT)

    for z in range(256):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                scr[x, y] = (x, y, z)

        scr.sync()
        time.sleep(0.1)