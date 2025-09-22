import picographics as pg 
import os
from pimoroni import Button

button_up = Button(22, invert=False)
button_down = Button(6, invert=False)
button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)

SCALE = 3
LINE_HEIGHT = 9
NUM_ROWS = 7
BUFFER_ROWS = 2

def get_app_list():
    app_list = []
    for file in os.listdir():
        if not file.endswith('.py'):
            continue
        if file == 'main.py':
            continue
        app_list.append(file.split('.')[0])
    return app_list

def menu():
    app_list = get_app_list()
    num_apps = len(app_list)
    display = pg.PicoGraphics(
        display=pg.DISPLAY_TUFTY_2040,
        pen_type=pg.PEN_RGB332
    )

    black_pen = display.create_pen(0, 0, 0)
    white_pen = display.create_pen(255, 255, 255)

    cursor_pos = 0
    scroll_pos = 0

    while True:

        display.set_pen(black_pen)
        display.clear()
        display.set_pen(white_pen)
        display.set_font('bitmap8')

        display.text('Pick an app!', 3, 3, scale=SCALE)

        for i, app in enumerate(app_list[scroll_pos:scroll_pos+NUM_ROWS]):
            # if i < scroll_pos or i >= scroll_pos + NUM_ROWS:
            #     continue
            display.text(app, 3+(7*SCALE), 42+(LINE_HEIGHT*SCALE*i), scale=SCALE)
        
        display.text('>', 3, 42+(LINE_HEIGHT*SCALE*(cursor_pos-scroll_pos)), scale=SCALE)
        
        display.update()

        pressed = False
        while not pressed:
            if button_down.read():
                pressed = True
                cursor_pos = (cursor_pos + 1) % num_apps
                if cursor_pos >= (scroll_pos + NUM_ROWS - BUFFER_ROWS):
                    scroll_pos += 1
                if cursor_pos < BUFFER_ROWS:
                    scroll_pos = 0
                if cursor_pos >= num_apps - BUFFER_ROWS:
                    scroll_pos = num_apps - NUM_ROWS 
            if button_up.read():
                pressed = True
                cursor_pos = (cursor_pos - 1) % num_apps
                if cursor_pos < (scroll_pos + BUFFER_ROWS):
                    scroll_pos -= 1
                if cursor_pos < BUFFER_ROWS:
                    scroll_pos = 0
                if cursor_pos >= num_apps - BUFFER_ROWS:
                    scroll_pos = num_apps - NUM_ROWS
            if button_a.read():
                return app_list[cursor_pos]


def cleanup():
    keep_these = [
        "__name__",
        "selected_app",
        "gc",
        "keep_these"
    ]
    import gc
    for k in locals().keys():
        if k not in keep_these:
            del locals()[k]
    gc.collect()


def main():
    selected_app = menu()
    cleanup()
    app = __import__(selected_app)
    app.main()


if __name__ == "__main__":
    main()