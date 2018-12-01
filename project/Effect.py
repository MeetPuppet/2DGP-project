from pico2d import *
import game_framework
import game_world
from enemyBullets import SuddenSpark, FireWall

# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 12

class Beat:
    image = None
    def __init__(self,point):
        self.x, self.y = point[0], point[1]
        self.frame = 0
        if Beat.image == None:
            Beat.image = load_image("image/effect/beat.png")

        pass
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) == 3:
            game_world.remove_object2(self, 10)
            pass
        pass
    def render(self):
        self.image.clip_draw(int(self.frame)*99,0,99,96,self.x, self.y)
        pass
    pass

class Smoke:
    image = None
    def __init__(self,point,isRight=True):
        self.x, self.y = point[0], point[1]
        self.frameX = 0
        if isRight:
            self.frameY = 0
        else:
            self.frameY = 1
        if Smoke.image == None:
            Smoke.image = load_image("image/effect/smoke.png")

        pass
    def update(self):
        self.frameX = (self.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frameX) == 5:
            game_world.remove_object2(self, 10)
            pass
        pass
    def render(self):
        self.image.clip_draw(int(self.frameX)*86,self.frameY*90,86,90,self.x, self.y)
        pass

class chargeSpark:
    image = None
    def __init__(self,point):
        self.x, self.y = point[0], point[1]
        self.frame = 0
        self.liveTime = 1
        if chargeSpark.image == None:
            chargeSpark.image = load_image("image/boss/kracko/readySpark.png")

        pass
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)%3
        self.liveTime -= game_framework.frame_time
        if self.liveTime < 0:
            game_world.add_object(SuddenSpark((self.x,self.y)),9)
            game_world.remove_object2(self, 10)
            pass
        pass
    def render(self):
        self.image.clip_draw(int(self.frame)*162,0,162,53,self.x, self.y)
        pass

class readyBurn:
    image = None
    def __init__(self):
        kirby= game_world.get_player_layer()[0]
        targetX = kirby.getPoint()[0]
        self.x, self.y = targetX, 24
        self.frame = 0
        self.liveTime = 2
        if readyBurn.image == None:
            readyBurn.image = load_image("image/boss/darkZero/burning.png")

        pass
    def update(self):
        kirby= game_world.get_player_layer()[0]
        targetX = kirby.getPoint()[0]

        if self.liveTime > 1:
            self.x = targetX

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)%4
        self.liveTime -= game_framework.frame_time
        if self.liveTime < 0:
            game_world.add_object(FireWall(self.x),9)
            game_world.remove_object2(self, 10)
            pass
        pass
    def render(self):
        self.image.clip_draw(int(self.frame)*48,0,48,48,self.x, self.y)
        pass