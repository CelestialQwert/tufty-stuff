import picographics as pg 

def main():
    display = pg.PicoGraphics(
        display=pg.DISPLAY_TUFTY_2040,
        pen_type=pg.PEN_RGB565
    )

    # black_pen = display.create_pen(0, 0, 0)
    # display.set_pen(black_pen)
    # display.clear()

    for i in range(256*256):
        # print(i)
        r = i // (2**11) * 8
        g = (i // 32) % 64 * 4
        b = (i % 32) * 8
        #print(r, g, b)
        display.set_pen(display.create_pen(r,g,b))

        x = (i % 320) 
        y = (i // 320)

        display.pixel(x, y)

        if not (i % 256):
            display.update()

    while True:
        pass

if __name__ == "__main__":
    main()