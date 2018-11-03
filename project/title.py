from pico2d import *

import inGame
import game_framework


name = "title"
front = None
image = None
anyKey = None
button = True
title_time = 0
alpha = 1

def enter():
    global image, front, anyKey
    front = load_image('image/black_screen.jpg')
    image = load_image('image/title.jpg')
    anyKey = load_image('image/press-any-key.png')


def exit():
    global image, front
    del(image)
    del(front)

def update():
    global front, title_time, alpha, button
    delay(0.1)
    if alpha > 0:
        alpha -= game_framework.frame_time
    else:
        alpha = 0

    if button == True:
        button = False
    else:
        button = True

    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif event.type == SDL_KEYDOWN:
                if event.key != SDLK_ESCAPE:
                    game_framework.change_state(inGame)
    pass


def draw():
    clear_canvas()
    image.draw(1024//2,768//2)
    if button == True:
        anyKey.draw(1024//2, 768-250)
    else:
        pass
    #front.draw(1024//2,768//2)
    update_canvas()
    pass
