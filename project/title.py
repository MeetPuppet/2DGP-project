from pico2d import *

import inGame
import game_framework

import game_world
from backGround import Stage

name = "title"
front = None
scene = -1
image0 = None
image1 = None
image2 = None
image3 = None
anyKey = None
button = True
title_time = 0
alpha = 1

def enter():
    global image1,image2,scene,image3, front, anyKey,title_time
    image0 = Stage()
    game_world.add_object(image0, 0)
    title_time = 0
    scene = -1
    front = load_image('image/title.png')
    image1 = load_image('image/title1.jpg')
    image2 = load_image('image/title2.jpg')
    image3 = load_image('image/title3.jpg')
    anyKey = load_image('image/press-any-key.png')


def exit():
    global image0, image1, image2, image3, front
    game_world.remove_object2(image0,0)
    del(image1)
    del(image2)
    del(image3)
    del(front)

def update():
    global front, title_time, alpha, button
    title_time+=game_framework.frame_time
    for game_object in game_world.all_objects():
        game_object.update()
    if alpha > 0:
        alpha -= game_framework.frame_time
    else:
        alpha = 0

    if scene ==-1:
        #if  button == True and int(title_time)%2==0:
         #   button = False
        #elif button == True and int(title_time)%2==0:
        button = True
    else:
        button = False

    pass

def handle_events():
    global scene
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif event.type == SDL_KEYDOWN:
                if event.key != SDLK_ESCAPE:
                    scene+=1
                    if scene == 3:
                        game_framework.change_state(inGame)
    pass


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.render()
    if scene == -1:
        front.draw(1024//2,384 + 100)
        pass
    elif scene == 0:
        image1.draw(1024//2,768//2)
    elif scene == 1:
        image2.draw(1024//2,768//2)
    else:
        image3.draw(1024//2,768//2)

    if button == True:
        anyKey.draw(1024//2, 300)
    else:
        pass
    #front.draw(1024//2,768//2)
    update_canvas()
    pass
