import curses
from screen import Screen


if __name__ == '__main__':
    WIDTH, HEIGHT = 48, 48

    win = curses.initscr()
    curses.noecho()

    scr = Screen(width=WIDTH, height=HEIGHT)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            scr[x, y] = (x, y, 0)

    scr.line(0, 0, 47, 47, (255,255,255))
    scr.line(47, 0, 0, 47, (255,255,255))
    render_distances = [6, 12, 16, 20]

    for d in render_distances:
        scr.rect(d, d, -d-1, -d-1, (255,0,0))

    while True:
        scr.sync()

        c = win.getch()
        print(c)
        assert False

    # WIDTH, HEIGHT = 48, 48



    scr.close()