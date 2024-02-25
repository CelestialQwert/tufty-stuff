import picographics as pg 
import pngdec
import time
# import machine

SCALE = 2

def main(display=None):
    if not display:
        display = pg.PicoGraphics(
            display=pg.DISPLAY_TUFTY_2040,
            pen_type=pg.PEN_RGB565
        )
    dec = pngdec.PNG(display)
    #machine.freq(int(190e6))


    display.set_backlight(.5)
    while True:
        for i in range(1,22):
            # print(f'start open {i}')
            dec.open_file(f"homer-pngtest/homer-bush-{i:04d}.png")
            # start = time.ticks_ms()
            dec.decode(0, 0, scale=(SCALE,SCALE))
            # print("decode took: {} ms".format(time.ticks_ms() - start))
            # print(f'start display {i}')
            # start = time.ticks_ms()
            display.update()
            # print("update took: {} ms".format(time.ticks_ms() - start))


if __name__ == '__main__':
    main()