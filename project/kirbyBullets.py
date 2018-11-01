from pico2d import *
import game_world
import game_framework

# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 150.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class kirbyBullet1:
    image = None
    def __init__(self, point  = (2000,2000)):
        self.x, self.y = point[0], point[1]
        self.size = 0
        self.damage = 1
        self.frame=0
        if kirbyBullet1.image == None:
            kirbyBullet1.image = load_image('image/kirby/kirbyBullet.png')
        pass
    def update(self):
        self.x += RUN_SPEED_PPS * game_framework.frame_time
        self.frame= (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        if self.x > 1074:
            game_world.remove_object2(self, 4)



        pass
    def render(self):
        self.image.clip_draw(int(self.frame)*72,0,72,10,self.x,self.y)
        pass


    def getX(self): return self.x
    def getKind(self): return self.size
    def getDamage(self): return self.damage
    pass

class kirbyBullet2:
    image = None
    def __init__(self, point  = (2000,2000)):
        self.x, self.y = point[0], point[1]
        self.size = 1
        self.damage = 4
        self.frame=0
        if kirbyBullet2.image == None:
            kirbyBullet2.image = load_image('image/kirby/kirbyBullet2.png')
        pass
    def update(self):
        self.x += (RUN_SPEED_PPS+(RUN_SPEED_PPS/3))*game_framework.frame_time
        self.frame= (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if self.x > 1074:
            game_world.remove_object2(self, 4)
        pass
    def render(self):
        self.image.clip_draw(int(self.frame)*126,0,126,48,self.x,self.y)
        pass


    def getX(self): return self.x
    def getKind(self): return self.size
    def getDamage(self): return self.damage
    pass

class maxBullet:
    image = None
    def __init__(self, point  = (2000,2000)):
        self.x, self.y = point[0], point[1]
        self.size = 2
        self.frame=0
        self.damage = 10
        if maxBullet.image == None:
            maxBullet.image = load_image('image/kirby/maxBullet.png')
        pass
    def update(self):
        self.x += (RUN_SPEED_PPS+(RUN_SPEED_PPS/2))*game_framework.frame_time
        self.frame= (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if self.x > 1074:
            game_world.remove_object2(self, 4)



        pass
    def render(self):
        self.image.clip_draw(int(self.frame)*232,0,232,150,self.x,self.y)
        pass


    def getX(self): return self.x
    def getKind(self): return self.size
    def getDamage(self): return self.damage
    pass

class starBullet:
    image = None
    def __init__(self, point  = (2000,2000)):
        self.x, self.y = point[0], point[1]
        self.damage = 5
        self.size = 1
        self.frame=0
        if starBullet.image == None:
            starBullet.image = load_image('image/kirby/StarBullet.png')
        pass
    def update(self):
        self.x += (RUN_SPEED_PPS+(RUN_SPEED_PPS/3))*game_framework.frame_time
        self.frame= (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if self.x > 1074:
            game_world.remove_object2(self, 4)
        pass
    def render(self):
        self.image.clip_draw(self.frame*30,0,30,30,self.x,self.y)
        pass


    def getX(self): return self.x
    def getKind(self): return self.size
    def getDamage(self): return self.damage
    pass

class kirbyBoom:
    def __init__(self,point  = (2000,2000)):
        self.x, self.y = point[0],point[1]
        self.activated = False
        self.limit = 5.0
        self.frame = 0
        self.readyImage = load_image("image/kirby/BoomBullet.png")
        self.actImage = load_image("image/kirby/BoomShot.png")
        self.readyImage.opacify(0.7)
        self.actImage.opacify(0.8)
        pass
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.limit -= game_framework.frame_time
        if self.limit < 1.0:
            self.activated = True

        if self.activated == False:
            self.x+=(RUN_SPEED_PPS/40)*game_framework.frame_time
        else:
            self.x+=(RUN_SPEED_PPS/60)*game_framework.frame_time
        if self.limit < 0:
            game_world.remove_object2(self, 5)
        pass
    def render(self):
        if self.activated == False:
            self.readyImage.clip_draw(int(self.frame)*46,0,46,46,self.x,self.y)
        else:
            self.actImage.clip_draw(int(self.frame)*512,0,512,512,self.x,self.y)
        pass

    def getPoint(self): return (self.x,self.y)
    def boomActivate(self): self.activated = True
    def getLimitTime(self): return self.limit
    pass