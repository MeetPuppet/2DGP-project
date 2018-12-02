from pico2d import *
import game_world
import game_framework
from kirbyBullets import kirbyBullet1, kirbyBullet2

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 12

class Shooter:
    image = None
    def __init__(self, point):
        self.x, self.y = point[0], point[1]
        self.frame = 0
        if Shooter.image == None:
            Shooter.image = load_image('image/kirby/shooter.png')
        pass
    def update(self,point):
        self.x, self.y = point[0], point[1]
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        pass
    def render(self):
        self.image.clip_draw(int(self.frame) * 66, 0 , 66, 36, self.x, self.y)

    def fireBullet(self, kind=0):
        if kind == 0:
            bullet = kirbyBullet1((self.x, self.y))
        else:
            bullet = kirbyBullet2((self.x, self.y))
        game_world.add_object(bullet,3)
    pass