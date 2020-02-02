import curses
from screen import Screen
from world import LEVEL

WIDTH, HEIGHT = 48, 48

KEY_W = 119
KEY_D = 100
KEY_A = 97
KEY_S = 115
KEY_E = 101


COLORS = [
    (230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 190), (0, 128, 128), (230, 190, 255), (170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180), (0, 0, 128), (128, 128, 128), (255, 255, 255)
]

def random_color(x, y, blink):
    i = (7*x+y)% len(COLORS)
    if blink:
        return COLORS[i] + (True,)
    return COLORS[i]
    
def darken(color, factor):
    r, g, b, *bb = color
    return (
        int(r * factor),
        int(g * factor),
        int(b * factor),
        bb[0] if bb else False,
    )

class Player:
    DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    DISTANCES = [0, 6, 12, 16, 20, 23, 24]

    def __init__(self, world):
        self.x = 0
        self.y = 0
        self.dir = 0
        self.world = world
    
    def rotate(self, orientation: int):
        self.dir = (self.dir + orientation) % 4

    def forward(self, dir_=1):
        x, y = 2*self.x+1, 2*self.y+1
        x += self.DIRS[self.dir][0]*dir_
        y += self.DIRS[self.dir][1]*dir_

        if self.world[y][x] == ' ':
            self.x += self.DIRS[self.dir][0]*dir_
            self.y += self.DIRS[self.dir][1]*dir_

    def backward(self):
        self.forward(-1)

    def interact(self):
        x, y = 2*self.x+1+self.DIRS[self.dir][0], 2*self.y+1+self.DIRS[self.dir][1]
        if 0 <= x < len(self.world[0]) and 0 <= y < len(self.world) and self.world[y][x] == 'X':
            self.world[y][x] = '#'            


    def render(self, screen):
        for i in range(HEIGHT//2):
            screen.hline(0, WIDTH-1, i, darken((183, 225, 243), 1 - 0.5*i / HEIGHT))

        for i in range(HEIGHT//2, HEIGHT):
            screen.hline(0, WIDTH-1, i, darken((170, 211, 86), 0.3 + 0.7*(i/HEIGHT)) )

        # screen.line(0, 0, WIDTH-1, HEIGHT-1, (255,255,255))
        # screen.line(0, HEIGHT-1, WIDTH-1, 0, (255,255,255))

        
        # for d in self.DISTANCES:
        #     screen.rect(d, d, -d-1, -d-1, (255,0,0, True))

        for dist, d in reversed(list(enumerate(self.DISTANCES[1:], 1))):
            # render front
            x = 2*self.x+1 + (2*dist-1)*self.DIRS[self.dir][0]
            y = 2*self.y+1 + (2*dist-1)*self.DIRS[self.dir][1]

            if 0 <= x < len(self.world[0]) and 0 <= y < len(self.world) and self.world[y][x] in 'X#':
                screen.fullrect(d, d, -d-1, -d-1, darken(
                    random_color(x,y, self.world[y][x] == 'X'),
                    0.5 + 0.5*(1-(d/(WIDTH//2)))
                ))

            # render left
            x -= self.DIRS[self.dir][0]
            y -= self.DIRS[self.dir][1]

            x += self.DIRS[(self.dir-1)%4][0]
            y += self.DIRS[(self.dir-1)%4][1]

            if 0 <= x < len(self.world[0]) and 0 <= y < len(self.world) and self.world[y][x] in 'X#':
                for xx in range(self.DISTANCES[dist-1], d):
                    screen.vline(xx, xx, -xx-1, darken(
                        random_color(x,y, self.world[y][x] == 'X'), 
                        0.5 + 0.5 * (1-(xx/(WIDTH//2)))
                    ))

            # render right 
            x -= 2*self.DIRS[(self.dir-1)%4][0]
            y -= 2*self.DIRS[(self.dir-1)%4][1]
            
            if 0 <= x < len(self.world[0]) and 0 <= y < len(self.world) and self.world[y][x] in 'X#':
                for xx in range(self.DISTANCES[dist-1], d):
                    screen.vline(WIDTH-1 - xx, xx, -xx-1, darken(
                        random_color(x,y, self.world[y][x] == 'X'),
                        0.5 + 0.5 * (1-(xx/(WIDTH//2)))
                    ))

        screen.puttext(1, 1, 'WSNE 3789', (255,0,0,True))
        screen.sync()


def render_view(screen, player, world):
    pass


if __name__ == '__main__':
    win = curses.initscr()
    curses.noecho()

    scr = Screen(width=WIDTH, height=HEIGHT)
    hero = Player(LEVEL)
    hero.render(scr)

    while True:
        hero.render(scr)

        c = win.getch()
        
        if c == KEY_W:
            hero.forward()
        if c == KEY_S:
            hero.backward()

        if c == KEY_A:
            hero.rotate(-1)
        if c == KEY_D:
            hero.rotate(1)
        if c == KEY_E:
            hero.interact()

    # WIDTH, HEIGHT = 48, 48



    # scr.close()