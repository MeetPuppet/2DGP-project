from pico2d import *
import game_world
import game_framework
import random
import math

# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Coin:
    image = None
    def __init__(self, point = (2000,2000)):
        self.x, self.y = point[0],point[1]
        self.dirX, self.dirY = -12,9
        self.angle = random.randint(0,628)/100
        self.itemNum = 0
        self.frame=0
        self.liveTime=10.0
        if Coin.image == None:
            Coin.image = load_image("image/item/coin.png");
            pass
        pass
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 9
        self.x+=math.cos(self.angle) * RUN_SPEED_PPS* game_framework.frame_time
        if self.x>1024-10 or self.x<0+10:
            self.angle = 3.141592-self.angle
        elif self.x > 1024 :
            self.x = 1024-10

        self.y+= -math.sin(self.angle)*RUN_SPEED_PPS* game_framework.frame_time
        if(self.y>768-10 or self.y<0+10):
            self.angle = -self.angle

        self.liveTime-=game_framework.frame_time

        if self.liveTime < 0:
            game_world.remove_object2(self, 3)
        pass
    def render(self):
        if self.liveTime < 4 and self.frame%3==0:
            pass
        else:
            self.image.clip_draw(int(self.frame)*32,0,32,32,self.x,self.y)
        pass
    pass

    def getPoint(self): return (self.x, self.y)
    def getItemNum(self): return self.itemNum
    def getLiveTime(self): return self.liveTime

class PowerUp:
    image = None

    def __init__(self, point= (2000,2000)):
        self.x, self.y = point[0], point[1]
        self.dirX, self.dirY = 12, 9
        self.angle = random.randint(0,628)/100
        self.itemNum = 1
        self.frame = 0
        self.liveTime = 10.0
        if PowerUp.image == None:
            PowerUp.image = load_image("image/item/PowerUp.png")
            pass
        pass

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x += math.cos(self.angle)  * RUN_SPEED_PPS* game_framework.frame_time
        if (self.x > 1024 - 10 or self.x < 0 + 10):
            self.angle = 3.141592-self.angle
        elif self.x > 1024:
            self.x = 1024 - 10

        self.y += -math.sin(self.angle)  * RUN_SPEED_PPS* game_framework.frame_time
        if (self.y > 768 - 10 or self.y < 0 + 10):
            self.angle = -self.angle

        self.liveTime -= game_framework.frame_time
        if self.liveTime < 0:
            game_world.remove_object2(self, 3)
        pass

    def render(self):
        if self.liveTime < 2 and int(self.frame) % 3 == 0:
            pass
        else:
            self.image.draw(self.x, self.y)
        pass

    pass

    def getPoint(self): return (self.x, self.y)
    def getItemNum(self): return self.itemNum
    def getLiveTime(self): return self.liveTime

class BoomUp:
    image = None
    def __init__(self, point = (2000,2000)):
        self.x, self.y = point[0],point[1]
        self.dirX, self.dirY = -12,9
        self.angle = random.randint(0,628)/100
        self.itemNum = 2
        self.frame = 0
        self.liveTime=10.0
        if BoomUp.image == None:
            BoomUp.image = load_image("image/item/Boom.png");
            pass
        pass
    def update(self):

        self.frame=(self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x+=math.cos(self.angle)  * RUN_SPEED_PPS* game_framework.frame_time
        if(self.x>1024-10 or self.x<0+10):
            self.angle = 3.141592-self.angle
        elif self.x > 1024 :
            self.x = 1024-10

        self.y+= -math.sin(self.angle) * RUN_SPEED_PPS* game_framework.frame_time
        if(self.y>768-10 or self.y<0+10):
            self.angle = -self.angle

        self.liveTime-=game_framework.frame_time
        pass
    def render(self):
        if self.liveTime < 2 and int(self.frame)%3==0:
            pass
        else:
            self.image.draw(self.x,self.y)
        pass
    pass

    def getPoint(self): return (self.x, self.y)
    def getItemNum(self): return self.itemNum
    def getLiveTime(self): return self.liveTime
