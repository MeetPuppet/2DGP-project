from pico2d import *

from UI import ScoreBoard, Numbers

import json
import game_framework
import title

rank1=None
rank2=None
rank3=None
rank4=None
rank5=None
numbers = []
image = None
sound = None

def enter():
    global sound, rank1,rank2, rank3, rank4, rank5, image, numbers
    image = load_image("image/rank.jpg")
    sound = load_music("sound/end.wav")
    sound.play()
    data_list=None
    with open('data.json', 'r') as f:
        data_list = json.load(f)
    rank1=ScoreBoard((512,700),data_list[0]["score"])
    rank2=ScoreBoard((512,650),data_list[1]["score"])
    rank3=ScoreBoard((512,600),data_list[2]["score"])
    rank4=ScoreBoard((512,550),data_list[3]["score"])
    rank5=ScoreBoard((512,500),data_list[4]["score"])
    numbers += [Numbers() for i in range(5)]

    pass


def exit():
    sound.stop()
    pass

def update():
    data_list=None
    with open('data.json', 'r') as f:
        data_list = json.load(f)
    rank1.update()
    rank2.update()
    rank3.update()
    rank4.update()
    rank5.update()
    i=1
    for number in numbers:
        number.update(i)
        i+=1
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
                    game_framework.change_state(title)
    pass


def draw():
    #clear_canvas()
    image.draw(1024//2,786//2)
    rank1.render()
    rank2.render()
    rank3.render()
    rank4.render()
    rank5.render()
    i=0
    for number in numbers:
        number.render((100,700-(i*50)))
        i+=1
    update_canvas()
    pass