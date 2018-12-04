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

from boss import Batafire, kracko, darkZero
from minions import Scarfy
from minions import SirKibble
from minions import blueClay
from minions import sunny

from enemyBullets import enemyBullet,Fireball,SirKibbleCutter, DarkStar, SuddenSpark ,FireWall

from Effect import Beat, readyBurn

#phase Range
ONE, TWO, THREE, BOSS = range(4)

#playCheck
realTime = 0
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
boss2 = None
boss3 = None

EBullet = None
fireball = None
Cutter = None
fireWall = None
spark =None

BGM = None

waves = [[[],[],[],[],[]],[[],[],[]],[[],[]]]
REDBOOL = [[[],[],[],[],[]],[[],[],[]],[[],[]]]
waveCount=0



def enter():
    global player, stage, bullet1, bullet2, bulletMax, star, boom, coins, powerUp, boomUp, fireWall, spark
    global minion1, minion2, boss1,boss2,boss3, EBullet, fireball, Cutter, waves, waveCount, REDBOOL, BGM

    BGM = load_music("sound/Green_Greens.wav")
    BGM.set_volume(64)
    player = Kirby()
    stage = Stage()
    bullet1 = kirbyBullet1()
    bullet2 = kirbyBullet2()
    bulletMax = maxBullet()
    star = starBullet()
    boom = kirbyBoom()
    fireWall = FireWall((0,0))
    spark =SuddenSpark((0,0))
    playTime = 0

    coins = Coin()
    powerUp = PowerUp((1024//2, 768//2))
    boomUp = BoomUp()
    minion2 = SirKibble()
    boss1 = Batafire()
    boss2 = kracko()
    boss3 = darkZero()

    EBullet = enemyBullet((1024//2, 768//2),player.getPoint())
    fireball = Fireball((1024//2, 768//2),player.getPoint())
    Cutter = SirKibbleCutter((1024//2, 768//2))

    game_world.add_object(stage, 0)
    game_world.add_object(player, 1)
    #minion1 = [Scarfy(0),Scarfy(1),Scarfy(2),Scarfy(3)]


    waves[0][0] += [Scarfy(2)for i in range(5)]
    REDBOOL[0][0] += [0 for i in range(5)]
    waves[0][1] += [Scarfy(3)for i in range(5)]
    REDBOOL[0][1] += [0 for i in range(5)]
    waves[0][2] += [Scarfy(0,(1074+i*500,384-(i*50))) for i in range(3)]
    waves[0][2] += [SirKibble() for i in range(3)]
    REDBOOL[0][2] += [0 for i in range(6)]
    waves[0][3] += [Scarfy(1,(1074+i*500,384+i*50)) for i in range(3)]
    waves[0][3] += [SirKibble() for i in range(3)]
    REDBOOL[0][3] += [0 for i in range(6)]
    waves[0][4] += [Batafire()]
    REDBOOL[0][4] += [0]
    waves[1][0] += [sunny()for i in range(3)]
    waves[1][0] += [blueClay()for i in range(5)]
    REDBOOL[1][0] += [False for i in range(8)]
    waves[1][1] += [kracko()]
    REDBOOL[1][1] += [0]
    waves[2][0] += [darkZero()]
    REDBOOL[2][0] += [0]
    BGM.play()
    pass


def exit():
    BGM.stop()
    game_world.clear()
    pass


def pause():
    pass


def resume():
    pass


num = 0

def handle_events():
    global waveCount, player, num
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)

        if event.type == SDL_KEYDOWN and event.key == SDLK_1:
            game_world.add_object(Coin((1024//2, 768//2)), 7)
            game_world.add_object(PowerUp((1024//2, 768//2)), 7)
            game_world.add_object(BoomUp((1024//2, 768//2)), 7)
            num=0

            pass
        if event.type == SDL_KEYDOWN and event.key == SDLK_2:
            game_world.add_object(Scarfy(0),4)
            game_world.add_object(Scarfy(1), 4)
            game_world.add_object(Scarfy(2), 4)
            game_world.add_object(SirKibble(),4)
            game_world.add_object(blueClay(), 4)
            game_world.add_object(sunny(), 4)
            num = 1
            #player.Hit()
            pass
        if event.type == SDL_KEYDOWN and event.key == SDLK_3:
            game_world.add_object(Fireball((1024//2, 768//2),player.getPoint()), 8)
            game_world.add_object(enemyBullet((1024//2, 768//2),player.getPoint()), 8)
            game_world.add_object(SirKibbleCutter((1024//2, 768//2)), 8)
            game_world.add_object(DarkStar(), 8)
            num = 2
            pass
        if event.type == SDL_KEYDOWN and event.key == SDLK_4:
            game_world.add_object(Batafire(), 5)
            pass
        if event.type == SDL_KEYDOWN and event.key == SDLK_5:
            game_world.add_object(boss2, 5)
            pass
        if event.type == SDL_KEYDOWN and event.key == SDLK_6:
            game_world.add_object(darkZero(), 5)
            #boss1.Kill()


i=0
j=0
bossCount=0
BOOLL = [False,False,False]
def update():
    global playTime, waveCount, i,j, stage, BOOLL
    global boss1, boss2, boss3, num, realTime, bossCount
    game_world.CommunicateObjects()


    stage.setStage(num)

    playTime += game_framework.frame_time*100
    if int(playTime) % 10 == 0 and i < len(waves[num][waveCount]) and waveCount < len(waves[num]):
        if num == 0 and waveCount == 4 and BOOLL[0] == False:
            game_world.add_object(waves[num][waveCount][i], 5)
            BOOLL[0] = True
        elif num == 1 and waveCount == 1 and BOOLL[1] == False:
            game_world.add_object(waves[num][waveCount][i], 5)
            BOOLL[1] = True
        elif num == 2 and waveCount == 0 and BOOLL[2] == False:
            game_world.add_object(waves[num][waveCount][i], 5)
            BOOLL[2] = True
        elif (num == 0 and waveCount < 4) or (num == 1 and waveCount < 1) :
            game_world.add_object(waves[num][waveCount][i], 4)
            i += 1
    elif int(playTime) % 250 == 0 and waveCount < len(waves[num]) - 1:
        waveCount += 1
        i = 0

    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.render()
    update_canvas()

def setStageNum(n):
    global num, waveCount, i
    num = n
    waveCount=0
    i = 0