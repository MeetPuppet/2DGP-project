from pico2d import *
import random
import rankTable
import json

from kirbyBullets import kirbyBullet1
from kirbyBullets import kirbyBullet2
from kirbyBullets import maxBullet
from kirbyBullets import starBullet
from kirbyBullets import kirbyBoom

from supporter import Shooter

from UI import kirbyHPUI
from UI import kirbyLifeUI
from UI import kirbyBoomUI
from UI import ScoreBoard

import game_world
import game_framework

def WINSIZEX(): return 1024
def WINSIZEY(): return 768

life = 2
gameScore = 0
# move Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 50.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

UP_KEY_DOWN, UP_KEY_UP, DOWN_KEY_DOWN, DOWN_KEY_UP, \
LEFT_KEY_DOWN, LEFT_KEY_UP, RIGHT_KEY_DOWN, RIGHT_KEY_UP,\
Z_KEY_DOWN, Z_KEY_UP, X_KEY_DOWN, \
CHARGE, BE_IDLE, SHOT, DEAD = range(15)


key_event_table = {
    (SDL_KEYDOWN, SDLK_UP): UP_KEY_DOWN,
    (SDL_KEYUP, SDLK_UP)  : UP_KEY_UP,

    (SDL_KEYDOWN, SDLK_DOWN): DOWN_KEY_DOWN,
    (SDL_KEYUP, SDLK_DOWN)  : DOWN_KEY_UP,

    (SDL_KEYDOWN, SDLK_LEFT): LEFT_KEY_DOWN,
    (SDL_KEYUP, SDLK_LEFT)  : LEFT_KEY_UP,

    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_KEY_DOWN,
    (SDL_KEYUP, SDLK_RIGHT)  : RIGHT_KEY_UP,

    (SDL_KEYDOWN, SDLK_z): Z_KEY_DOWN,
    (SDL_KEYUP, SDLK_z): Z_KEY_UP,

    (SDL_KEYDOWN, SDLK_x): X_KEY_DOWN,
}

class EventState:

    @staticmethod
    def enter(Kirby, event):
        Kirby.isEvent = True
        Kirby.guard = 3
        pass

    @staticmethod
    def exit(Kirby, event):
        pass

    @staticmethod
    def do(Kirby):
        Kirby.frameX = (Kirby.frameX + Kirby.FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        Kirby.x += (RUN_SPEED_PPS/10) * game_framework.frame_time
        if Kirby.x > 100 and Kirby.HP > 0 :
            Kirby.isEvent = False
            Kirby.add_event(BE_IDLE)

    @staticmethod
    def draw(Kirby):
        Kirby.IDLE.clip_draw(int(Kirby.frameX)*48,0,48,40,Kirby.x,Kirby.y)

class IdleState:

    @staticmethod
    def enter(Kirby, event):
        if event == UP_KEY_DOWN:
            Kirby.dirY = RUN_SPEED_PPS
        elif event == UP_KEY_UP and Kirby.dirY > 0:
            Kirby.dirY = 0
        elif event == DOWN_KEY_DOWN:
            Kirby.dirY = -RUN_SPEED_PPS
        elif event == DOWN_KEY_UP and Kirby.dirY < 0:
            Kirby.dirY = 0


        if event == LEFT_KEY_DOWN:
            Kirby.dirX = -RUN_SPEED_PPS
        elif event == LEFT_KEY_UP and Kirby.dirX < 0:
            Kirby.dirX = 0
        elif event == RIGHT_KEY_DOWN:
            Kirby.dirX = RUN_SPEED_PPS
        elif event == RIGHT_KEY_UP and Kirby.dirX > 0:
            Kirby.dirX = 0


    @staticmethod
    def exit(Kirby, event):
        if event == Z_KEY_DOWN:
            if Kirby.grog == False:
                Kirby.Bullet1()
            else:
                Kirby.StarBullet()
            Kirby.countOn = True
        elif event == Z_KEY_UP:
            Kirby.chargeCount = 0
            Kirby.countOn = False
            pass
        if event == X_KEY_DOWN:
            if Kirby.boom > 0:
                Kirby.Boom()
                Kirby.boom-=1
        pass

    @staticmethod
    def do(Kirby):
        if Kirby.HP <= 0 :
            Kirby.add_event(DEAD)
        Kirby.FRAMES_PER_ACTION = 8
        if Kirby.countOn == True:
            Kirby.chargeCount += game_framework.frame_time

        if Kirby.chargeCount >= 1:
            Kirby.add_event(CHARGE)

        Kirby.frameX = (Kirby.frameX + Kirby.FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        Kirby.x = Kirby.x + game_framework.frame_time * Kirby.dirX
        if Kirby.x > 1024 - 24 or Kirby.x < 0 + 24:
            Kirby.x = Kirby.x - game_framework.frame_time * Kirby.dirX
        Kirby.y = Kirby.y + game_framework.frame_time * Kirby.dirY
        if Kirby.y > 768 - 24 or Kirby.y < 0 + 24:
            Kirby.y = Kirby.y - game_framework.frame_time * Kirby.dirY
        # fill here

    @staticmethod
    def draw(Kirby):
        Kirby.IDLE.clip_draw(int(Kirby.frameX)*48,0,48,40,Kirby.x,Kirby.y)

class MoveState:

    @staticmethod
    def enter(Kirby, event):
        if event == UP_KEY_DOWN:
            Kirby.dirY = RUN_SPEED_PPS
        elif event == UP_KEY_UP and Kirby.dirY > 0:
            Kirby.dirY = 0
        elif event == DOWN_KEY_DOWN:
            Kirby.dirY = -RUN_SPEED_PPS
        elif event == DOWN_KEY_UP and Kirby.dirY < 0:
            Kirby.dirY = 0


        if event == LEFT_KEY_DOWN:
            Kirby.dirX = -RUN_SPEED_PPS
        elif event == LEFT_KEY_UP and Kirby.dirX < 0:
            Kirby.dirX = 0
        elif event == RIGHT_KEY_DOWN:
            Kirby.dirX = RUN_SPEED_PPS
        elif event == RIGHT_KEY_UP and Kirby.dirX > 0:
            Kirby.dirX = 0


    @staticmethod
    def exit(Kirby, event):
        if event == Z_KEY_DOWN:
            if Kirby.grog == False:
                Kirby.Bullet1()
            else:
                Kirby.StarBullet()
            Kirby.countOn = True
        elif event == Z_KEY_UP:
            Kirby.chargeCount = 0
            Kirby.countOn = False
            pass

        if event == X_KEY_DOWN:
            if Kirby.boom > 0:
                Kirby.Boom()
                Kirby.boom-=1
        pass

    @staticmethod
    def do(Kirby):
        if Kirby.HP <= 0 :
            Kirby.add_event(DEAD)
        Kirby.FRAMES_PER_ACTION = 8

        if Kirby.countOn == True:
            Kirby.chargeCount += game_framework.frame_time

        if Kirby.chargeCount >= 1:
            Kirby.add_event(CHARGE)

        Kirby.frameX = (Kirby.frameX + Kirby.FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        Kirby.x = Kirby.x + game_framework.frame_time * Kirby.dirX
        if Kirby.x > 1024 - 24 or Kirby.x < 0 + 24:
            Kirby.x = Kirby.x - game_framework.frame_time * Kirby.dirX
        Kirby.y = Kirby.y + game_framework.frame_time * Kirby.dirY
        if Kirby.y > 768 - 24 or Kirby.y < 0 + 24:
            Kirby.y = Kirby.y - game_framework.frame_time * Kirby.dirY
        # fill here

    @staticmethod
    def draw(Kirby):
        Kirby.IDLE.clip_draw(int(Kirby.frameX)*48,0,48,40,Kirby.x,Kirby.y)


class ReadyState:

    @staticmethod
    def enter(Kirby, event):
        if event == UP_KEY_DOWN:
            Kirby.dirY = RUN_SPEED_PPS
        elif event == UP_KEY_UP and Kirby.dirY > 0:
            Kirby.dirY = 0
        elif event == DOWN_KEY_DOWN:
            Kirby.dirY = -RUN_SPEED_PPS
        elif event == DOWN_KEY_UP and Kirby.dirY < 0:
            Kirby.dirY = 0


        if event == LEFT_KEY_DOWN:
            Kirby.dirX = -RUN_SPEED_PPS
        elif event == LEFT_KEY_UP and Kirby.dirX < 0:
            Kirby.dirX = 0
        elif event == RIGHT_KEY_DOWN:
            Kirby.dirX = RUN_SPEED_PPS
        elif event == RIGHT_KEY_UP and Kirby.dirX > 0:
            Kirby.dirX = 0
    @staticmethod
    def exit(Kirby, event):
        if event == Z_KEY_UP:
            if Kirby.frameY == 1:
                #level2
                Kirby.Bullet2()
                Kirby.countOn = False
                Kirby.frameY = 0
                Kirby.chargeCount = 0
                Kirby.FRAMES_PER_ACTION = 8
                Kirby.add_event(BE_IDLE)
                pass
            elif Kirby.frameY == 2:
                #level3
                Kirby.MaxBullet()
                Kirby.countOn = False
                Kirby.frameY = 0
                Kirby.chargeCount = 0
                Kirby.FRAMES_PER_ACTION = 8
                Kirby.add_event(SHOT)
            else:
                pass



        if event == X_KEY_DOWN:
            if Kirby.boom > 0:
                Kirby.Boom()
                Kirby.boom-=1
        pass

    @staticmethod
    def do(Kirby):
        if Kirby.HP <= 0 :
            Kirby.add_event(DEAD)
        Kirby.FRAMES_PER_ACTION = 6
        Kirby.frameX = (Kirby.frameX + Kirby.FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        Kirby.chargeCount += game_framework.frame_time

        if Kirby.frameY == 0 and int(Kirby.frameX) == 3:
            Kirby.frameY = 1
        elif Kirby.chargeCount >= 3:
            Kirby.frameY = 2

        Kirby.x = Kirby.x + game_framework.frame_time * Kirby.dirX
        if Kirby.x > 1024 - 24 or Kirby.x < 0 + 24:
            Kirby.x = Kirby.x - game_framework.frame_time * Kirby.dirX
        Kirby.y = Kirby.y + game_framework.frame_time * Kirby.dirY
        if Kirby.y > 768 - 24 or Kirby.y < 0 + 24:
            Kirby.y = Kirby.y - game_framework.frame_time * Kirby.dirY
        # fill here

    @staticmethod
    def draw(Kirby):
        Kirby.CHARGE.clip_draw(int(Kirby.frameX)*64,Kirby.frameY*64,64,64,Kirby.x,Kirby.y)

class ShotState:

    @staticmethod
    def enter(Kirby, event):
        if event == UP_KEY_DOWN:
            Kirby.dirY = RUN_SPEED_PPS
        elif event == UP_KEY_UP and Kirby.dirY > 0:
            Kirby.dirY = 0
        elif event == DOWN_KEY_DOWN:
            Kirby.dirY = -RUN_SPEED_PPS
        elif event == DOWN_KEY_UP and Kirby.dirY < 0:
            Kirby.dirY = 0


        if event == LEFT_KEY_DOWN:
            Kirby.dirX = -RUN_SPEED_PPS
        elif event == LEFT_KEY_UP and Kirby.dirX < 0:
            Kirby.dirX = 0
        elif event == RIGHT_KEY_DOWN:
            Kirby.dirX = RUN_SPEED_PPS
        elif event == RIGHT_KEY_UP and Kirby.dirX > 0:
            Kirby.dirX = 0

    @staticmethod
    def exit(Kirby, event):
        if event == Z_KEY_DOWN:
            if Kirby.grog == False:
                Kirby.Bullet1()
            else:
                Kirby.StarBullet()
            pass
        pass

        if event == X_KEY_DOWN:
            if Kirby.boom > 0:
                Kirby.Boom()
                Kirby.boom -= 1

    @staticmethod
    def do(Kirby):
        if Kirby.HP <= 0 :
            Kirby.add_event(DEAD)
        Kirby.FRAMES_PER_ACTION = 8

        Kirby.frameX = (Kirby.frameX + Kirby.FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if int(Kirby.frameX) == 7:
             Kirby.add_event(BE_IDLE)


        Kirby.x = Kirby.x + game_framework.frame_time * Kirby.dirX
        if Kirby.x > 1024 - 24 or Kirby.x < 0 + 24:
            Kirby.x = Kirby.x - game_framework.frame_time * Kirby.dirX
        Kirby.y = Kirby.y + game_framework.frame_time * Kirby.dirY
        if Kirby.y > 768 - 24 or Kirby.y < 0 + 24:
            Kirby.y = Kirby.y - game_framework.frame_time * Kirby.dirY
        # fill here

    @staticmethod
    def draw(Kirby):
        Kirby.MAX.clip_draw(int(Kirby.frameX)*120,0,120,80,Kirby.x,Kirby.y)

class DeadState:
    global life

    @staticmethod
    def enter(Kirby, event):
        Kirby.isEvent = True
        Kirby.deadSound.play()
        Kirby.guard = 3
        pass

    @staticmethod
    def exit(Kirby, event):
        pass

    @staticmethod
    def do(Kirby):
        global life
        Kirby.y -= (RUN_SPEED_PPS) * game_framework.frame_time
        if Kirby.y < -50 and life > 0:
            life-=1
            Kirby.__init__()

    @staticmethod
    def draw(Kirby):
        Kirby.IDLE.clip_draw(int(Kirby.frameX)*48,0,48,40,Kirby.x,Kirby.y)


next_state_table = {
    EventState: {UP_KEY_DOWN: EventState, UP_KEY_UP: EventState, DOWN_KEY_DOWN: EventState, DOWN_KEY_UP: EventState,
                LEFT_KEY_DOWN: EventState, LEFT_KEY_UP: EventState,RIGHT_KEY_DOWN: EventState, RIGHT_KEY_UP: EventState,
                Z_KEY_DOWN: EventState,Z_KEY_UP: EventState,X_KEY_DOWN: EventState, BE_IDLE: IdleState},

    IdleState: {UP_KEY_DOWN: MoveState, UP_KEY_UP: IdleState, DOWN_KEY_DOWN: MoveState, DOWN_KEY_UP: IdleState,
                LEFT_KEY_DOWN: MoveState, LEFT_KEY_UP: IdleState,RIGHT_KEY_DOWN: MoveState, RIGHT_KEY_UP: IdleState,
                Z_KEY_DOWN: IdleState,Z_KEY_UP: IdleState,X_KEY_DOWN: IdleState, CHARGE: ReadyState,DEAD: DeadState},

    MoveState: {UP_KEY_DOWN: MoveState, UP_KEY_UP: IdleState, DOWN_KEY_DOWN: MoveState, DOWN_KEY_UP: IdleState,
                LEFT_KEY_DOWN: MoveState, LEFT_KEY_UP: IdleState, RIGHT_KEY_DOWN: MoveState, RIGHT_KEY_UP: IdleState,
                Z_KEY_DOWN: MoveState, Z_KEY_UP: MoveState, X_KEY_DOWN: MoveState, CHARGE: ReadyState,DEAD: DeadState},

    ReadyState: {UP_KEY_DOWN: ReadyState, UP_KEY_UP: ReadyState, DOWN_KEY_DOWN: ReadyState, DOWN_KEY_UP: ReadyState,
                LEFT_KEY_DOWN: ReadyState, LEFT_KEY_UP: ReadyState,RIGHT_KEY_DOWN: ReadyState, RIGHT_KEY_UP: ReadyState,
                Z_KEY_DOWN: ReadyState, Z_KEY_UP: ReadyState, X_KEY_DOWN: ReadyState, BE_IDLE: IdleState, SHOT: ShotState
                , DEAD: DeadState},

    ShotState: {UP_KEY_DOWN: ShotState, UP_KEY_UP: ShotState, DOWN_KEY_DOWN: ShotState, DOWN_KEY_UP: ShotState,
                    LEFT_KEY_DOWN: ShotState, LEFT_KEY_UP: ShotState,RIGHT_KEY_DOWN: ShotState, RIGHT_KEY_UP: ShotState,
                    Z_KEY_DOWN: ShotState, Z_KEY_UP: IdleState, X_KEY_DOWN: ShotState, BE_IDLE: IdleState,DEAD: DeadState},

    DeadState: {UP_KEY_DOWN: DeadState, UP_KEY_UP: DeadState, DOWN_KEY_DOWN: DeadState, DOWN_KEY_UP: DeadState,
                LEFT_KEY_DOWN: DeadState, LEFT_KEY_UP: DeadState,RIGHT_KEY_DOWN: DeadState, RIGHT_KEY_UP: DeadState,
                Z_KEY_DOWN: DeadState,Z_KEY_UP: DeadState,X_KEY_DOWN: DeadState, BE_IDLE: IdleState}
}

class Kirby:
    scoreBoard = None
    bulletSound = None
    maxSound = None
    hurtSound = None
    deadSound = None
    getItems = None
    def __init__(self):
        if Kirby.bulletSound == None:
            Kirby.bulletSound = load_wav('sound/kriby/shot.wav')
        self.bulletSound.set_volume(64)
        if Kirby.maxSound == None:
            Kirby.maxSound = load_wav('sound/kriby/maxShot.wav')
        self.maxSound.set_volume(64)
        if Kirby.hurtSound == None:
            Kirby.hurtSound = load_wav('sound/kriby/hurt.wav')
        self.hurtSound.set_volume(64)
        if Kirby.deadSound == None:
            Kirby.deadSound = load_wav('sound/kriby/0361.wav')
        self.deadSound.set_volume(64)
        if Kirby.getItems == None:
            Kirby.getItems = load_wav('sound/kriby/getItems.wav')
        self.getItems.set_volume(64)
        self.x, self.y =-10.0,384.0
        self.radius = 20
        self.dirX, self.dirY = 0, 0
        self.frameX, self.frameY = 0, 0
        self.chargeCount = 0
        self.guard = 0
        self.countOn = False
        self.isEvent = True
        self.grog = False

        self.support = []
        self.supCount = 0

        self.maxHP = 5
        self.HP = 5
        self.HPUI = kirbyHPUI(self.HP)

        self.life = 2
        self.lifeUI = kirbyLifeUI(self.life)

        self.FRAMES_PER_ACTION = 8

        self.boom = 2
        self.boomUI = kirbyBoomUI(self.boom)

        if Kirby.scoreBoard == None:
            Kirby.scoreBoard = ScoreBoard()

        self.event_que = []
        self.cur_state = EventState
        self.cur_state.enter(self, None)
        self.IDLE = load_image('image/kirby/kirbyIDLE.png')
        self.CHARGE = load_image('image/kirby/chargeLevel.png')
        self.MAX = load_image('image/kirby/FullShot.png')
        #pass


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def update(self):
        if self.guard > 0:
            self.guard -= game_framework.frame_time
            alpha = random.randint(5,8)/10
            self.IDLE.opacify(alpha)
            self.CHARGE.opacify(alpha)
            self.MAX.opacify(alpha)
        else:
            self.IDLE.opacify(1)
            self.CHARGE.opacify(1)
            self.MAX.opacify(1)

        if self.HP == 5 and self.life == 2:
            self.scoreBoard.upScore(game_framework.frame_time*20)

        if self.HP==1:
            self.grog = True

        if self.grog == True:
            self.scoreBoard.upScore(game_framework.frame_time*20)

        self.scoreBoard.update()
        self.cur_state.do(self)

        self.HPUI.update(self.HP)
        self.lifeUI.update(self.life)
        self.boomUI.update(self.boom)

        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            if self.isEvent == False:
                self.cur_state = next_state_table[self.cur_state][event]
                self.cur_state.enter(self, event)

        if self.HP > self.maxHP:
            self.HP = self.maxHP

        i=0
        for shoot in self.support:
            shoot.update((self.x-70,self.y+(70-(i*140))))
            i+=1

        if self.HP <= 0 and self.life <= 0:
            score = int(self.scoreBoard.getScore())
            try:
                with open('data.json', 'r') as f:
                    data_list = json.load(f)
                for j in range(5):
                    for i in range(5):
                        if data_list[i]["score"] <= score:
                            data_list[i]["score"], score = score, data_list[i]["score"]
                f.close()
            except:
                data_list = [{"rank": 1, "score": 1000000},{"rank": 2, "score": 50000},{"rank": 3, "score": 30000},{"rank": 4, "score": 10000},{"rank": 5, "score": 5000}]
                for j in range(5):
                    for i in range(5):
                        if data_list[i]["score"] <= score:
                            data_list[i]["score"], score = score, data_list[i]["score"]
            with open('data.json', 'w') as f:
                json.dump(data_list, f)

            game_framework.change_state(rankTable)

    def render(self):
        self.cur_state.draw(self)
        self.HPUI.render()
        self.lifeUI.render()
        self.boomUI.render()
        self.scoreBoard.render()
        for shoot in self.support:
            shoot.render()
        #pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def Bullet1(self):
        # fill here
        bullet = kirbyBullet1((self.x, self.y))
        game_world.add_object(bullet,3)
        self.bulletSound.play()
        for shoot in self.support:
            shoot.fireBullet()
        pass

    def Bullet2(self):
        # fill here
        bullet = kirbyBullet2((self.x, self.y))
        game_world.add_object(bullet,3)
        self.bulletSound.play()
        for shoot in self.support:
            shoot.fireBullet()
        pass

    def MaxBullet(self):
        # fill here
        bullet = maxBullet((self.x, self.y))
        game_world.add_object(bullet,3)
        self.maxSound.play()
        for shoot in self.support:
            shoot.fireBullet(1)
        pass

    def StarBullet(self):
        # fill here
        bullet = starBullet((self.x, self.y))
        game_world.add_object(bullet,3)
        self.bulletSound.play()
        for shoot in self.support:
            shoot.fireBullet()
        pass

    def Boom(self):
        boom = kirbyBoom((self.x, self.y))
        game_world.add_object(boom, 6)

    def getPoint(self): return (self.x,self.y)
    def getRadius(self): return self.radius

    def getRect(self):
        return [(self.x-23,self.x+23,self.y-10,self.y+10),
                (self.x - 12, self.x + 12, self.y - 20, self.y + 20)]

    def getScore(self): return self.scoreBoard.getScore()
    def upScore(self):
        self.scoreBoard.upScore()

    def getHP(self): return self.HP
    def heal(self): self.HP += 1
    def Hit(self):
        if self.guard <= 0:
            self.HP -= 1
            Kirby.hurtSound.play()
            self.guard =3

    def getBoom(self): return self.boom
    def setBoom(self,count=1):
        Kirby.getItems.play()
        self.boom += count

    def getFrameY(self): return self.frameY
    def setFrameYZero(self): self.frameY=0

    def setDirectX(self, num): self.dirX += num
    def setDirectY(self, num): self.dirY += num

    def getCount(self): return self.chargeCount
    def isCharge(self, BOOL): self.countOn = BOOL
    def resetCount(self): self.chargeCount=0

    def onGrog(self): self.grog = True
    def offGrog(self): self.grog = False

    def summonShooter(self):
        Kirby.getItems.play()
        if self.supCount < 2:
            self.support += [Shooter((self.x,self.y))]
            self.supCount+=1
        else:
            self.scoreBoard.upScore(1000)

    pass