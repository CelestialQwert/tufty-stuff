def main():
    import picographics as pg 

    display = pg.PicoGraphics(
        display=pg.DISPLAY_TUFTY_2040,
        pen_type=pg.PEN_RGB332
    )

    black_pen = display.create_pen(0, 0, 0)
    white_pen = display.create_pen(255, 255, 255)

    display.set_pen(black_pen)
    display.set_font('bitmap8')

    display.clear()

    display.set_pen(white_pen)
    display.text('Dummy app', 2, 2, scale=4)
    display.update()

    while True:
        pass

if __name__ == "__main__":
    main()