from pico2d import *
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Stage:
    def __init__(self):
        self.frame1X, self.frame1Y =0,0
        self.frame2X, self.frame2Y =1024,0
        self.stage=0
        self.twisted = False
        self.image1 = load_image("image/map.jpg")
        self.image2 = load_image("image/map.jpg")
        pass
    def update(self):

        if self.stage ==0:
            moveRange =RUN_SPEED_PPS*game_framework.frame_time
            if self.frame1X < -(1024):
                self.frame1X += 2048 - moveRange
            else:
                self.frame1X -= moveRange

            if self.frame2X < -(1024):
                self.frame2X += 2048 - moveRange
            else:
                self.frame2X -= moveRange
        elif self.stage == 1:
            moveRange =RUN_SPEED_PPS/2*game_framework.frame_time
            if self.frame1X < -(1024):
                self.frame1X += 2048 - moveRange
            else:
                self.frame1X -= moveRange

            if self.frame2X < -(1024):
                self.frame2X += 2048 - moveRange
            else:
                self.frame2X -= moveRange
        elif self.stage ==2:
            moveRange =RUN_SPEED_PPS/2*game_framework.frame_time
            if self.frame1X < -(1024):
                self.frame1X += 2048 - moveRange
            else:
                self.frame1X -= moveRange

            if self.frame2X < -(1024):
                self.frame2X += 2048 - moveRange
            else:
                self.frame2X -= moveRange



        pass
    def render(self):
        self.image1.clip_draw(0,int(self.frame1Y),1024,768,self.frame1X+(1024//2),768//2)
        self.image2.clip_draw(0,int(self.frame2Y),1024,768,self.frame2X+(1024//2),768//2)



    def setStage(self, stage):
        self.stage=stage
        if self.stage ==0:
            if self.frame1Y > 0:
                self.frame1Y -= RUN_SPEED_PPS*game_framework.frame_time/2
                self.frame2Y -= RUN_SPEED_PPS*game_framework.frame_time/2
            else:
                self.frame1Y = 0
                self.frame2Y = 0
        elif self.stage == 1:
            if self.frame1Y > 768+RUN_SPEED_PPS*0.01:
                self.frame1Y -= RUN_SPEED_PPS*game_framework.frame_time/2
                self.frame2Y -= RUN_SPEED_PPS*game_framework.frame_time/2
            elif self.frame1Y < 768-RUN_SPEED_PPS*0.01:
                self.frame1Y += RUN_SPEED_PPS*game_framework.frame_time/2
                self.frame2Y += RUN_SPEED_PPS*game_framework.frame_time/2
            else:
                self.frame1Y = 768
                self.frame2Y = 768
        elif self.stage ==2:
            if self.frame1Y < 768 * 2+2:
                self.frame1Y += RUN_SPEED_PPS*game_framework.frame_time/2
                self.frame2Y += RUN_SPEED_PPS*game_framework.frame_time/2
            else:
                self.frame1Y = 768 * 2+2
                self.frame2Y = 768 * 2+2


    def twistedWorld(self):
        self.twisted = True
        pass
    pass
