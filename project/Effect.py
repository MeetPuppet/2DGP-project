from pico2d import *
import game_framework
import game_world

# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 12

class Beat:
    def __init__(self,point):
        self.x, self.y = point[0], point[1]
        self.frame = 0
        self.image = load_image("image/effect/beat.png")

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
    def __init__(self,point,isRight=True):
        self.x, self.y = point[0], point[1]
        self.frameX = 0
        if isRight:
            self.frameY = 0
        else:
            self.frameY = 1
        self.image = load_image("image/effect/smoke.png")

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
