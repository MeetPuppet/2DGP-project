from pico2d import *
import random
import game_world
import game_framework

from enemyBullets import enemyBullet
from enemyBullets import Fireball
from enemyBullets import SirKibbleCutter

# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 50.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Scarfy:
    image =None
    def __init__(self,moveNumber):
        self.pattern = moveNumber
        self.shotTime = 0.6
        self.radius = 25
        self.isDead = 0
        self.isDown = 0
        self.jumpPower = 8
        self.gravity = 100
        self.frame = 0
        self.liveTime = 0
        if moveNumber%2 == 0:
            self.x, self.y = 1074, 550+6
            self.stratPoint = (1074, 550)
            pass
        else:
            self.x, self.y = 1074, 250+6
            self.stratPoint = (1074, 250)
            pass

        if Scarfy.image == None:
            Scarfy.image = load_image("image/minion/scarfy.png")
            pass
        pass
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if self.shotTime > 0 : self.shotTime-=game_framework.frame_time
        else:
            #shot  +random.randint(-10,10)/10
            game_world.add_object(enemyBullet((self.x,self.y),(self.x-1,self.y)), 5)
            self.shotTime = 0.5
            pass

        if self. pattern == 0:
            self.x = ((2*self.liveTime**2-3*self.liveTime+1)*1074 + (-4*self.liveTime**2+4*self.liveTime)*350 + (2*self.liveTime**2-self.liveTime)*1074)
            self.y = ((2*self.liveTime**2-3*self.liveTime+1)*768 + (-4*self.liveTime**2+4*self.liveTime)*600 + (2*self.liveTime**2-self.liveTime)*350)
            self.liveTime+=game_framework.frame_time/2
            pass

        elif self.pattern == 1:
            self.x = ((2*self.liveTime**2-3*self.liveTime+1)*1074 + (-4*self.liveTime**2+4*self.liveTime)*350 + (2*self.liveTime**2-self.liveTime)*1074)
            self.y = ((2*self.liveTime**2-3*self.liveTime+1)*0 + (-4*self.liveTime**2+4*self.liveTime)*168 + (2*self.liveTime**2-self.liveTime)*418)
            self.liveTime+=game_framework.frame_time/2
            pass
        elif self. pattern >= 2:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time
            if self.stratPoint[1] + 15 > self.y:
                self.gravity = (RUN_SPEED_PPS/15)*game_framework.frame_time
                self.jumpPower += self.gravity
                self.y += self.jumpPower
                pass
            elif self.stratPoint[1] - 15 < self.y:
                self.gravity = (RUN_SPEED_PPS/15)*game_framework.frame_time
                self.jumpPower -= self.gravity
                self.y += self.jumpPower
                pass

        if self.x > 1074 or self.x < -50:
            game_world.remove_object2(self, 2)
            pass
        pass
    def render(self):
        self.image.clip_draw(int(self.frame)*50,0,50,50,self.x,self.y)
        pass

    def getRadius(self): return self.radius
    def getPoint(self): return (self.x, self.y)
    def getState(self): return self.isDead
    def Kill(self): self.isDead = 1
    def getSize(self): return 0
    def shotTiming(self): return self.shotTime

    pass

class SirKibble:
    image =None
    def __init__(self):
        self.x, self.y = random.randint(512,900), -100
        self.jumpPower = random.randint(20,28)
        self.radius = 32
        self.isDead = 0
        self.frame = 0
        if SirKibble.image == None:
            SirKibble.image = load_image("image/minion/SirKibble.png")
            pass
        pass
    def update(self):
        if self.frame == 0 :
            self.y = self.y+self.jumpPower
            self.jumpPower-=(RUN_SPEED_PPS/15)*game_framework.frame_time
            if self.jumpPower < 0:
                self.frame = 1
        elif self.frame == 3:
            self.y = self.y+self.jumpPower
            self.jumpPower-=(RUN_SPEED_PPS/15)*game_framework.frame_time
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)%3
            if int(self.frame) == 2:
                game_world.add_object(SirKibbleCutter((self.x, self.y)), 5)
                self.frame = 3

        if self.y < 0 and self.frame == 3:
            game_world.remove_object2(self, 2)
        pass
    def render(self):
        self.image.clip_draw(int(self.frame)*72,0,72,72,self.x,self.y)
        pass

    def getRadius(self): return self.radius
    def getPoint(self): return (self.x, self.y)
    def getState(self): return self.isDead
    def Kill(self): self.isDead = 1
    def getFrame(self): return self.frame
    pass
