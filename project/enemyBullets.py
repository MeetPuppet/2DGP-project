from pico2d import *

import game_world
import game_framework
import math

# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 80.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

def getDistance(startPoint, endPoint):
    Xdistance = startPoint[0] - endPoint[0]
    Ydistance = startPoint[1] - endPoint[1]
    return math.sqrt(Xdistance**2+Ydistance**2)

def getAngle(startPoint, endPoint):

    Xdistance = endPoint[0] - startPoint[0]
    Ydistance = endPoint[1] - startPoint[1]
    distance = math.sqrt(Xdistance ** 2 + Ydistance ** 2)

    angle = math.acos(Xdistance / distance)

    if endPoint[1] > startPoint[1] :
        angle = (3.141592*2) - angle
        if angle > (3.141592*2):
            angle -= (3.141592*2)

    return angle

    pass

class enemyBullet:
    image =None
    def __init__(self, startPoint, wayPoint):
        self.start = startPoint
        self.x, self.y = startPoint[0], startPoint[1]
        self.radius = 12
        self.dir = RUN_SPEED_PPS
        self.wayPoint = wayPoint
        self.angle = getAngle(startPoint, wayPoint)
        if enemyBullet.image == None:
            enemyBullet.image = load_image("image/minion/bullet.png")
        pass
    def update(self):

        self.x += math.cos(self.angle) * self.dir* game_framework.frame_time

        self.y += -math.sin(self.angle) * self.dir * game_framework.frame_time

        if self.x > getDistance(self.start,(self.x,self.y)):
            game_world.remove_object2(self,6)
        pass
    def render(self):
        self.image.draw(self.x, self.y)
        pass

    def getRadius(self): return self.radius
    def bulletRemoverChecker(self):
        if getDistance(self.start,(self.x,self.y)) > 1000:
            return True
        return False
    pass

class SirKibbleCutter:
    image =None
    def __init__(self, startPoint):
        self.start = startPoint
        self.x, self.y = startPoint[0], startPoint[1]
        self.radius = 24
        self.frame = 0
        self.dir = RUN_SPEED_PPS+(RUN_SPEED_PPS/1.5)
        if SirKibbleCutter.image == None:
            SirKibbleCutter.image = load_image("image/minion/SirKibbleCutter.png")
        pass
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.x -= self.dir * game_framework.frame_time
        if self.x > -20:
            game_world.remove_object2(self,6)

    def render(self):
        self.image.clip_draw(int(self.frame)*69,0,69,48,self.x,self.y)
        pass

    def getRadius(self): return self.radius
    def bulletRemoverChecker(self):
        if getDistance(self.start,(self.x,self.y)) > 1000:
            return True
        return False
    pass

class Fireball:
    image =None
    def __init__(self, startPoint, wayPoint):
        self.start = startPoint
        self.x, self.y = startPoint[0], startPoint[1]
        self.radius = 36
        self.frame = 0
        self.dir = RUN_SPEED_PPS
        self.wayPoint = wayPoint
        self.angle = getAngle(startPoint, wayPoint)
        if Fireball.image == None:
            Fireball.image = load_image("image/boss/fireBall.png")
        pass
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        self.x += math.cos(self.angle) * self.dir* game_framework.frame_time

        self.y += -math.sin(self.angle) * self.dir * game_framework.frame_time

        if self.x > getDistance(self.start,(self.x,self.y)):
            game_world.remove_object2(self,6)
        pass
    def render(self):
        self.image.clip_draw(int(self.frame)*72,0,72,72,self.x,self.y)
        pass

    def getRadius(self): return self.radius
    def bulletRemoverChecker(self):
        if getDistance(self.start,(self.x,self.y)) > 1000:
            return True
        return False
    pass