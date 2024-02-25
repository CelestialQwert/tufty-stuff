import picographics as pg 

def main():
    display = pg.PicoGraphics(
        display=pg.DISPLAY_TUFTY_2040,
        pen_type=pg.PEN_RGB332
    )

    # black_pen = display.create_pen(0, 0, 0)
    # display.set_pen(black_pen)
    # display.clear()

    for i in range(256):
        # print(i)
        r = i // (2**5) * 32
        g = (i // 4) % 8 * 32
        b = i % 4 * 64
        # print(r, g, b)
        display.set_pen(display.create_pen(r,g,b))

        x = (i % 16) * 15
        y = (i // 16) * 15

        display.rectangle(40+x, y, 15, 15)

    display.update()

    while True:
        pass

if __name__ == "__main__":
    main()