from pico2d import *

from kirbyBullets import kirbyBullet1
from kirbyBullets import kirbyBullet2
from kirbyBullets import maxBullet
from kirbyBullets import starBullet
from kirbyBullets import kirbyBoom

import game_world
import game_framework

def WINSIZEX(): return 1024
def WINSIZEY(): return 768


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
CHARGE, BE_IDLE, SHOT = range(14)


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
        pass

    @staticmethod
    def exit(Kirby, event):
        if event == Z_KEY_DOWN:
            Kirby.Bullet1()
        pass

    @staticmethod
    def do(Kirby):
        Kirby.frameX = (Kirby.frameX + Kirby.FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        Kirby.x = Kirby.x + (RUN_SPEED_PPS/10) * game_framework.frame_time
        if Kirby.x > 100:
            Kirby.isEvent = False
            Kirby.add_event(BE_IDLE)
        # fill here

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
            Kirby.Bullet1()
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
            Kirby.Bullet1()
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
        Kirby.FRAMES_PER_ACTION = 6
        Kirby.frameX = (Kirby.frameX + Kirby.FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        Kirby.chargeCount += game_framework.frame_time

        if Kirby.frameY == 0 and int(Kirby.frameX) == 3:
            Kirby.frameY = 1
        elif Kirby.chargeCount >= 3:
            Kirby.frameY = 2

        if Kirby.x > 1024 - 24 or Kirby.x < 0 + 24:
            Kirby.x = Kirby.x - game_framework.frame_time * Kirby.dirX
        else:
            Kirby.x = Kirby.x + game_framework.frame_time * Kirby.dirX
        if Kirby.y > 768 - 24 or Kirby.y < 0 + 24:
            Kirby.y = Kirby.y - game_framework.frame_time * Kirby.dirY
        else:
            Kirby.y = Kirby.y + game_framework.frame_time * Kirby.dirY
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
            #kirbyBullet
            Kirby.Bullet1()
            pass
        pass

    @staticmethod
    def do(Kirby):
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


next_state_table = {
    EventState: {UP_KEY_DOWN: EventState, UP_KEY_UP: EventState, DOWN_KEY_DOWN: EventState, DOWN_KEY_UP: EventState,
                LEFT_KEY_DOWN: EventState, LEFT_KEY_UP: EventState,RIGHT_KEY_DOWN: EventState, RIGHT_KEY_UP: EventState,
                Z_KEY_DOWN: EventState,Z_KEY_UP: EventState,X_KEY_DOWN: EventState, BE_IDLE: IdleState},

    IdleState: {UP_KEY_DOWN: MoveState, UP_KEY_UP: IdleState, DOWN_KEY_DOWN: MoveState, DOWN_KEY_UP: IdleState,
                LEFT_KEY_DOWN: MoveState, LEFT_KEY_UP: IdleState,RIGHT_KEY_DOWN: MoveState, RIGHT_KEY_UP: IdleState,
                Z_KEY_DOWN: IdleState,Z_KEY_UP: IdleState,X_KEY_DOWN: IdleState, CHARGE: ReadyState},

    MoveState: {UP_KEY_DOWN: IdleState, UP_KEY_UP: IdleState, DOWN_KEY_DOWN: IdleState, DOWN_KEY_UP: IdleState,
                LEFT_KEY_DOWN: IdleState, LEFT_KEY_UP: IdleState, RIGHT_KEY_DOWN: IdleState, RIGHT_KEY_UP: IdleState,
                Z_KEY_DOWN: MoveState, Z_KEY_UP: MoveState, X_KEY_DOWN: MoveState, CHARGE: ReadyState},

    ReadyState: {UP_KEY_DOWN: ReadyState, UP_KEY_UP: ReadyState, DOWN_KEY_DOWN: ReadyState, DOWN_KEY_UP: ReadyState,
                LEFT_KEY_DOWN: ReadyState, LEFT_KEY_UP: ReadyState,RIGHT_KEY_DOWN: ReadyState, RIGHT_KEY_UP: ReadyState,
                Z_KEY_DOWN: ReadyState, Z_KEY_UP: ReadyState, X_KEY_DOWN: ReadyState, BE_IDLE: IdleState, SHOT: ShotState},

    ShotState: {UP_KEY_DOWN: ShotState, UP_KEY_UP: ShotState, DOWN_KEY_DOWN: ShotState, DOWN_KEY_UP: ShotState,
                    LEFT_KEY_DOWN: ShotState, LEFT_KEY_UP: ShotState,RIGHT_KEY_DOWN: ShotState, RIGHT_KEY_UP: ShotState,
                    Z_KEY_DOWN: ShotState, Z_KEY_UP: ShotState, X_KEY_DOWN: ShotState, BE_IDLE: IdleState}
}

class Kirby:
    def __init__(self):
        self.x, self.y =-10.0,384.0
        self.radius = 20
        self.dirX, self.dirY = 0, 0
        self.frameX, self.frameY = 0, 0
        self.chargeCount = 0
        self.countOn = False
        self.isEvent = True
        self.maxHP = 5
        self.HP = 5
        self.FRAMES_PER_ACTION = 8
        self.boom = 2
        self.event_que = []
        self.cur_state = EventState
        self.cur_state.enter(self, None)
        self.IDLE = load_image('image/kirby/kirbyIDLE.png')
        self.CHARGE = load_image('image/kirby/chargeLevel.png')
        self.MAX = load_image('image/kirby/FullShot.png')
        #pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            if self.isEvent == False:
                self.cur_state = next_state_table[self.cur_state][event]
                self.cur_state.enter(self, event)

        if self.HP > self.maxHP:
            self.HP = self.maxHP



    def render(self):
        self.cur_state.draw(self)
        #pass

    def Bullet1(self):
        # fill here
        bullet = kirbyBullet1((self.x, self.y))
        game_world.add_object(bullet,4)
        pass

    def Bullet2(self):
        # fill here
        bullet = kirbyBullet2((self.x, self.y))
        game_world.add_object(bullet,4)
        pass

    def MaxBullet(self):
        # fill here
        bullet = maxBullet((self.x, self.y))
        game_world.add_object(bullet,4)
        pass

    def StarBullet(self):
        # fill here
        bullet = starBullet((self.x, self.y))
        game_world.add_object(bullet,4)
        pass

    def Boom(self):
        boom = kirbyBoom((self.x, self.y))
        game_world.add_object(boom, 5)

    def getPoint(self): return (self.x,self.y)
    def getRadius(self): return self.radius

    def getHP(self): return self.HP
    def heal(self): self.HP += 1
    def hit(self): self.HP -= 1

    def getBoom(self): return self.boom
    def setBoom(self,count): self.boom += count

    def getFrameY(self): return self.frameY
    def setFrameYZero(self): self.frameY=0

    def setDirectX(self, num): self.dirX += num
    def setDirectY(self, num): self.dirY += num

    def getCount(self): return self.chargeCount
    def isCharge(self, BOOL): self.countOn = BOOL
    def resetCount(self): self.chargeCount=0


    pass