from pico2d import *
import game_framework
import game_world

import enum
import random
import math

from Kirby import Kirby

from kirbyBullets import kirbyBullet1
from kirbyBullets import kirbyBullet2
from kirbyBullets import maxBullet
from kirbyBullets import starBullet
from kirbyBullets import kirbyBoom

from backGround import Stage

from Items import Coin
from Items import PowerUp
from Items import BoomUp

from boss import Batafire
from minions import Scarfy
from minions import SirKibble

from enemyBullets import enemyBullet
from enemyBullets import Fireball
from enemyBullets import SirKibbleCutter

from Effect import Beat

#phase Range
ONE, TWO, THREE, BOSS = range(4)

#playCheck
playTime = 0

#debug
NUM_ONE, NUM_TWO, NUM_THREE, NUM_FOUR,NUM_FIVE = range(5)

key_event_table = {
    (SDL_KEYDOWN, SDLK_1): NUM_ONE,
    (SDL_KEYDOWN, SDLK_2): NUM_TWO,
    (SDL_KEYDOWN, SDLK_3): NUM_THREE,
    (SDL_KEYDOWN, SDLK_4): NUM_FOUR,
    (SDL_KEYDOWN, SDLK_5): NUM_FIVE,
}

name = 'inGame'

running = True
player = None
stage = None

coins = None
powerUp = None
boomUp = None

bullet1 = None
bullet2 = None
bulletMax = None
star = None
boom =None

minion1 = None
minion2 = None
boss1 = None

EBullet = None
fireball = None
Cutter = None

waves = [[],[],[],[],[],[]]
waveCount=0

class UI:#maybe unused

    def __init__(self, inGame, type):

        pass
    def update(self):
        pass
    def render(self):
        self.a=0
    pass



def enter():
    global player, stage, bullet1, bullet2, bulletMax, star, boom, coins, powerUp, boomUp
    global minion1, minion2, boss1, EBullet, fireball, Cutter, waves, waveCount
    player = Kirby()
    stage = Stage(0)
    bullet1 = kirbyBullet1()
    bullet2 = kirbyBullet2()
    bulletMax = maxBullet()
    star = starBullet()
    boom = kirbyBoom()

    coins = Coin()
    powerUp = PowerUp((1024//2, 768//2))
    boomUp = BoomUp()

    #minion1 = [Scarfy(0),Scarfy(1),Scarfy(2),Scarfy(3)]
    minion2 = SirKibble()
    boss1 = Batafire()

    EBullet = enemyBullet((1024//2, 768//2),player.getPoint())
    fireball = Fireball((1024//2, 768//2),player.getPoint())
    Cutter = SirKibbleCutter((1024//2, 768//2))

    game_world.add_object(stage, 0)
    game_world.add_object(player, 1)

    waves[0] += []
    waves[1] += [Scarfy(2)for i in range(5)]
    waves[2] += [Scarfy(3)for i in range(5)]
    waves[3] += [Scarfy(0,(1074+i*500,384-(i*50))) for i in range(3)]
    waves[3] += [SirKibble() for i in range(3)]
    waves[4] += [Scarfy(1,(1074+i*500,384+i*50)) for i in range(3)]
    waves[4] += [SirKibble() for i in range(3)]
    waves[5] += [Batafire()]

    pass


def exit():
    game_world.clear()
    pass


def pause():
    pass


def resume():
    pass




def handle_events():
    global waveCount
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)

        if event.type == SDL_KEYDOWN and event.key == SDLK_1:
            game_world.add_object(Coin((1024//2, 768//2)), 3)
            game_world.add_object(PowerUp((1024//2, 768//2)), 3)
            game_world.add_object(BoomUp((1024//2, 768//2)), 3)

            pass
        if event.type == SDL_KEYDOWN and event.key == SDLK_2:
            game_world.add_object(Scarfy(0), 2)
            game_world.add_object(Scarfy(1), 2)
            game_world.add_object(Scarfy(2), 2)
            game_world.add_object(Scarfy(3), 2)
            game_world.add_object(SirKibble(), 2)
            pass
        if event.type == SDL_KEYDOWN and event.key == SDLK_3:
            game_world.add_object(Fireball((1024//2, 768//2),player.getPoint()), 5)
            game_world.add_object(enemyBullet((1024//2, 768//2),player.getPoint()), 5)
            game_world.add_object(SirKibbleCutter((1024//2, 768//2)), 5)
            pass
        if event.type == SDL_KEYDOWN and event.key == SDLK_4:
            game_world.add_object(Batafire(), 2)
            pass
        if event.type == SDL_KEYDOWN and event.key == SDLK_5:
            boss1.Kill()
            pass
        if event.type == SDL_KEYDOWN and event.key == SDLK_6:
            game_world.add_object(Beat((1024//2, 768//2)), 7)

i=0

def update():
    global playTime, waveCount, i
    game_world.intersectRectToRect()
    game_world.intersectDistance()
    if waveCount != 6:
        playTime+=1
    if playTime%10 == 0 and i < len(waves[waveCount]) and waveCount < len(waves):
            game_world.add_object(waves[waveCount][i], 2)
            i+=1
    if playTime % 200 == 0 and waveCount < len(waves)-1:
        waveCount+=1
        i = 0



    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.render()
    update_canvas()

