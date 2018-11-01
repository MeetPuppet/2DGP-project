from pico2d import *
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Stage:
    def __init__(self, stage):
        if stage == 0:
            self.frame1X, self.frame1Y =0,0
            self.frame2X, self.frame2Y =1024,0
        elif stage == 1:
            self.frame1X, self.frame1Y =0,1
            self.frame2X, self.frame2Y =1024,1
        else:
            self.frame1X, self.frame1Y =0,2
            self.frame2X, self.frame2Y =1024,2
        self.image1 = load_image("image/map.jpg")
        self.image2 = load_image("image/map.jpg")
        pass
    def update(self):
        moveRange =RUN_SPEED_PPS*game_framework.frame_time

        if self.frame1X < -1004:
            self.frame1X = self.frame2X + 1004
        else:
            self.frame1X -= moveRange

        if self.frame2X < -1004:
            self.frame2X = self.frame1X + 1004
        else:
            self.frame2X -= moveRange

        pass
    def render(self):
        self.image1.clip_draw(0,self.frame1Y*768,1024,768,self.frame1X+(1024//2),768//2)
        self.image2.clip_draw(0,self.frame2Y*768,1024,768,self.frame2X+(1024//2),768//2)
        pass
    pass
