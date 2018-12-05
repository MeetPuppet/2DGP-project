from pico2d import *

import random
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
        self.radius = 15
        self.dir = RUN_SPEED_PPS
        self.wayPoint = wayPoint
        self.angle = getAngle(startPoint, wayPoint)
        if enemyBullet.image == None:
            enemyBullet.image = load_image("image/minion/bullet.png")
        pass
    def update(self):
        self.x += math.cos(self.angle) * self.dir* game_framework.frame_time

        self.y += -math.sin(self.angle) * self.dir * game_framework.frame_time

        if self.x < 0 or self.x>1024:
            game_world.remove_object2(self,8)
        pass
    def render(self):
        self.image.draw(self.x, self.y)
        pass

    def getPoint(self): return (self.x,self.y)
    def getRect(self):
        return [(self.x-12,self.x+12,self.y-(6),self.y+(6)),
                (self.x+6,self.x+6,self.y-(12),self.y+(12))]
    def getRadius(self): return self.radius
    def bulletRemoverChecker(self):
        if getDistance(self.start,(self.x,self.y)) > 1000:
            return True
        return False
    def setAngle(self, angle): self.angle = angle
    def removeBullet(self):
            game_world.remove_object2(self,8)

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
        if self.x < -20:
            game_world.remove_object2(self,8)

    def render(self):
        self.image.clip_draw(int(self.frame)*69,0,69,48,self.x,self.y)
        pass

    def getPoint(self): return (self.x,self.y)
    def getRect(self):
        return [(self.x-34,self.x+34,self.y-(12),self.y+(12)),
                (self.x+17,self.x+17,self.y-(24),self.y+(24))]
    def getRadius(self): return self.radius
    def bulletRemoverChecker(self):
        if getDistance(self.start,(self.x,self.y)) > 1000:
            return True
        return False

    def removeBullet(self):
            game_world.remove_object2(self,8)
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

        if 1000 < getDistance(self.start,(self.x,self.y)):
            game_world.remove_object2(self,8)
        pass
    def render(self):
        self.image.clip_draw(int(self.frame)*72,0,72,72,self.x,self.y)
        pass

    def getPoint(self): return (self.x,self.y)
    def getRect(self):
        return [(self.x-36,self.x+36,self.y-(18),self.y+(18)),
                (self.x-18,self.x+18,self.y-(36),self.y+(36))]
    def getRadius(self): return self.radius
    def bulletRemoverChecker(self):
        if getDistance(self.start,(self.x,self.y)) > 1000:
            return True
        return False

    def removeBullet(self):
            game_world.remove_object2(self,8)
    pass

class DarkStar:
    image = None
    def __init__(self):
        self.radius = 36
        self.frameX = 0
        self.isRight = random.randint(0,1)
        if self.isRight == 0:
            self.x, self.y = 1124, random.randint(50,718)
            pass
        else:
            self.x, self.y = -100, random.randint(50,718)
            pass
        if DarkStar.image == None:
            DarkStar.image = load_image("image/boss/darkZero/darkStar.png")
        pass
    def update(self):
        self.frameX = (self.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)%4

        if self.isRight == 0:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time
            pass
        else:
            self.x += RUN_SPEED_PPS * game_framework.frame_time
            pass

        if self.x < -300 or self.x > 1024+300:
            game_world.remove_object2(self,8)

        pass

    def render(self):
        self.image.clip_draw(int(self.frameX)*69,self.isRight*72,69,72,self.x,self.y)




        pass

    def getPoint(self): return (self.x,self.y)
    def getRect(self):
        return [(self.x-35,self.x+35,self.y-(36),self.y+(36)),
                (self.x-35,self.x+35,self.y-(36),self.y+(36))]
    def getRadius(self): return self.radius
    def removeBullet(self):
            game_world.remove_object2(self,8)
    pass

class SuddenSpark:
    image = None
    sound = None
    def __init__(self, point):
        if SuddenSpark.sound == None:
            SuddenSpark.sound = load_wav("sound/kracko/song383.wav")
        self.x, self.y = point[0], point[1]
        self.radius = 30
        self.frame = 0
        self.liveTime = 0.5
        if SuddenSpark.image == None:
            SuddenSpark.image = load_image("image/boss/kracko/spark.png")
        self.soundPlay()
        pass
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

        self.liveTime -= game_framework.frame_time

        if self.liveTime < 0:
            game_world.remove_object2(self,9)
        pass
    def render(self):
        self.image.clip_draw(int(self.frame)*128,0,128,60,self.x,self.y)
        pass

    def getPoint(self): return (self.x,self.y)
    def getRect(self):
        return [(self.x-64,self.x+64,self.y-(25),self.y+(25)),
                (self.x-64,self.x+64,self.y-(25),self.y+(25))]
    def getRadius(self): return self.radius
    def removeBullet(self):
            game_world.remove_object2(self,9)
    def soundPlay(self):
        self.sound.play()
    pass
    pass

class FireWall:
    readyImage = None
    image = None
    def __init__(self, X):
        self.x, self.y = X, 768//2
        self.radius = 30
        self.frame = 0
        self.burn = False
        self.liveTime = 2
        if FireWall.image == None:
            FireWall.readyImage = load_image("image/boss/darkZero/fireReady.png")
            FireWall.image = load_image("image/boss/darkZero/fireWall.png")
        pass
    def update(self):
        if self.burn == False:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            if int(self.frame) == 3:
                self.burn = True
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)%4


        self.liveTime -= game_framework.frame_time

        if self.liveTime < 0:
            game_world.remove_object2(self,9)
        pass
    def render(self):
        if self.burn == False:
            self.readyImage.clip_draw(int(self.frame)*324,0,324,768,self.x,self.y)
        else:
            self.image.clip_draw(int(self.frame)*324,0,324,768,self.x,self.y)



        pass

    def getPoint(self): return (self.x,self.y)
    def getRect(self):
        if self.burn == False:
            return [(self.x-71,self.x+71,self.y-(384),self.y-(364)),
                (self.x-71,self.x+71,self.y-(384),self.y-(364))]
        else:
            return [(self.x-132,self.x+132,self.y-(384),self.y+(384)),
                (self.x-132,self.x+132,self.y-(384),self.y+(384))]
    def getRadius(self): return self.radius
    def removeBullet(self):
            game_world.remove_object2(self,9)
    pass
    pass