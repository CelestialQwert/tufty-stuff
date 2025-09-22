import jpegdec
import os
import random
import time
import picographics as pg 
from pimoroni import Button

TEXT_SCALE = 2

CYCLE_SPEEDS = [3000, 5000, 10000, 15000]

MANUAL = 0
SLIDESHOW = 1
SHUFFLE = 2

PICROOTDIR = 'pics'

button_up = Button(22, invert=False)
button_down = Button(6, invert=False)
button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
      

def main():
    display = pg.PicoGraphics(
        display=pg.DISPLAY_TUFTY_2040,
        pen_type=pg.PEN_RGB565
    )
            
    jp = jpegdec.JPEG(display)
    
    black_pen = display.create_pen(0, 0, 0)
    white_pen = display.create_pen(255, 255, 255)
    display.set_backlight(0.5)
    display.set_font('bitmap8')

    pic_dirs = [PICROOTDIR]
    for root_thing in os.ilistdir(PICROOTDIR):
        filename, filetype, _, _ = root_thing
        if filetype == 0x4000:
            pic_dirs.append(f'{PICROOTDIR}/{filename}')

    numdirs = len(pic_dirs)
    dirnum = numdirs - 1

    picfiles = []
    numfiles = 0
    picnum = 0
    
    new_dir = True
    new_pic = True
    new_message = False
    message_showing = False
    slideshow = MANUAL
    
    mticks = 0 # message ticks
    sticks = 0 # slideshow ticks
    speed_idx = len(CYCLE_SPEEDS) - 1
    cycle_speed = CYCLE_SPEEDS[speed_idx]
    message = ''
    shuffle_deck = []
    
    while True:

        if new_dir:
            while True:
                dirnum = (dirnum + 1) % numdirs
                current_dir = pic_dirs[dirnum]
                files = os.listdir(current_dir)
                files = [
                    {
                        'path': f'{current_dir}/{file}',
                        'name': file.split('.')[0]
                    }
                    for file in files if file.endswith('.jpg')
                ]
                picfiles = sorted(files, key=lambda x:x['name'])
                
                numfiles = len(picfiles)
                picnum = 0
                if numfiles != 0:
                    break
            new_pic = True
            new_dir = False
            slideshow = 0
        
        if new_pic:
            jp.open_file(picfiles[picnum]['path'])
            jp.decode()
            new_pic = False
            if not slideshow:
                picname = picfiles[picnum]['name']
                dirname = current_dir.split('/')[-1]
                message = f'{dirname} - {picname}'
                new_message = True
            else: 
                # only update here, otherwise there's a new message that 
                # will also cause an update... two updates causes a small
                # flicker before the message appears
                display.update()
        
        if new_message:          
            # w = display.measure_text(message, TEXT_SCALE)
            display.set_pen(black_pen)
            #display.rectangle(0, 0, w+4, 20)
            display.rectangle(0, 0, 320, 20)
            display.set_pen(white_pen)
            display.text(message, 2, 2, scale=TEXT_SCALE)
            display.update()
            message_showing = True
            mticks = time.ticks_ms()
            new_message = False
        
        if message_showing:
            if time.ticks_ms() - mticks > 1000:
                jp.decode()
                display.update()
                message_showing = False
        
        if slideshow:
            if time.ticks_ms() - sticks > cycle_speed:
                sticks = time.ticks_ms()
                if slideshow == SLIDESHOW:
                    picnum = (picnum + 1) % numfiles
                else:
                    pick = random.randint(0, len(shuffle_deck)-1)
                    picnum = shuffle_deck.pop(pick)
                    if len(shuffle_deck) < numfiles:
                        shuffle_deck += list(range(numfiles))
                new_pic = True
        
        if button_up.read():
            picnum = (picnum - 1) % numfiles
            new_pic = True
            slideshow = False
            
        if button_down.read():
            picnum = (picnum + 1) % numfiles
            new_pic = True
            slideshow = False
        
        if button_a.read():
            slideshow = (slideshow + 1) % 3
            if slideshow == 0:
                message = 'Mode MANUAL'
            elif slideshow == 1:
                message = 'Mode SLIDESHOW'
                sticks = time.ticks_ms()
            else:
                message = 'Mode SHUFFLE'
                sticks = time.ticks_ms()
                shuffle_deck = list(range(numfiles)) * 2
            new_message = True
        
        if button_b.read():
            if slideshow:
                speed_idx = (speed_idx + 1) % len(CYCLE_SPEEDS)
                cycle_speed = CYCLE_SPEEDS[speed_idx]
                message = f'Pic time {cycle_speed//1000} seconds'
                new_message = True
        
        if button_c.read():
            new_dir = True

if __name__ == '__main__':
    main()