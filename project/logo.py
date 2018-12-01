from pico2d import *

import title
import game_framework


name = "logo"
front = None
image = None
logo_time = 0
alpha = 0.0

def enter():
    global image, front
    front = load_image('image/black_screen.png')
    image = load_image('image/kpu_credit.png')
    front.opacify(0)


def exit():
    global image, front
    del(image)
    del(front)

def update():
    global front, logo_time, alpha
    logo_time += game_framework.frame_time
    if logo_time < 1:
        if alpha < 1:
            alpha += game_framework.frame_time/2
            front.opacify(alpha)
        else:
            pass
    elif logo_time > 2:
        if alpha > 0:
            alpha -= game_framework.frame_time/2
            front.opacify(alpha)
        else:
            front.opacify(0)
            game_framework.change_state(title)

    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
    pass


def draw():
    clear_canvas()
    image.draw(1024//2,768//2)
    #front.draw(1024 // 2, 768 // 2)
    update_canvas()
    pass
