from pico2d import *
import game_world
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import random


from UI import bossGause
from enemyBullets import Fireball, enemyBullet, getAngle
from minions import miniBata
from Effect import Smoke


# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Batafire:
    IDLE = None
    READY = None
    FIRE = None
    CHARGE = None
    DEAD = None
    def __init__(self):
        self.x, self.y = 1500,768//2
        self.maxHP, self.HP = 200, 200
        self.radius = 90
        self.frame = 0
        self.state = 0
        self.guarding = 1
        self.wait = 10
        self.backMove = False
        self.UpMove = False
        self.count = 0
        self.falling = RUN_SPEED_PPS
        self.gause = None
        #실행초에 어딘가 이미지를 로드해놓고 교체하는 방식이라면
        if Batafire.IDLE == None:
            Batafire.IDLE = load_image("image/boss/batafireIDLE.png")
        if Batafire.READY == None:
            Batafire.READY = load_image("image/boss/batafireReady.png")
        if Batafire.FIRE == None:
            Batafire.FIRE = load_image("image/boss/batafireFire.png")
        if Batafire.CHARGE == None:
            Batafire.CHARGE = load_image("image/boss/batafireCharge.png")
        if Batafire.DEAD == None:
            Batafire.DEAD = load_image("image/boss/batafireDead.png")

        pass
    def update(self):
        if self.gause == None:
            self.gause = bossGause(self.maxHP)
        else:
            self.gause.update(self.HP)

        if self.HP <= 0: self.state = 4

        if self.state == 0:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10

            if self.backMove == True:
                self.x+=RUN_SPEED_PPS*game_framework.frame_time
            else:
                self.x-=RUN_SPEED_PPS*game_framework.frame_time
            if self.x > 974:
                if self.UpMove == True:
                    self.y+=RUN_SPEED_PPS*game_framework.frame_time
                else:
                    self.y-=RUN_SPEED_PPS*game_framework.frame_time

            if self.x < 612:
                self.backMove = True
                pass
            elif self.x > 974:
                self.backMove = False
                pass
            if self.y > 718:
                self.UpMove = False
                pass
            elif self.y < 100:
                self.UpMove = True
                pass


            self.wait -= game_framework.frame_time
            if self.wait < 0:
                self.frame = 0
                self.state = 1
            pass

        elif self.state == 1:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            if int(self.frame) == 3:
                for i in range(3): game_world.add_object(miniBata((1300,random.randint(100,668))),2)
                if random.randint(0,1) == 0:
                    self.state = 2
                    self.wait = 3
                else:
                    self.state = 3
                self.frame = 0
            pass

        elif self.state == 2:
            self.wait -= game_framework.frame_time
            self.count += game_framework.frame_time
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
            if self.count / 0.1 > 1:
                game_world.add_object(Fireball((self.x-100,self.y-100),(self.x-200,self.y-100+random.randint(-100,100))), 8)
                self.count = 0

            if self.wait < 0:
                self.wait = 10
                self.frame = 0
                self.state = 0
                pass
            pass
        elif self.state == 3:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
            if self.x > -300 :
                self.x-=(RUN_SPEED_PPS*6)*game_framework.frame_time
            else:
                self.wait = 10
                self.frame = 0
                self.x = 1300
                self.state = 0

            pass
        elif self.state == 4:
            if self.falling > 0 : self.frame = 0
            else : self.frame = 1

            self.y+=self.falling*game_framework.frame_time
            self.falling-=(RUN_SPEED_PPS)*game_framework.frame_time

            if self.falling > -1 :
                get_time()

            if self.y < -150:
                game_world.remove_object2(self, 5)

            pass
        pass
    def render(self):
        self.gause.render()
        if self.state == 0:
            self.IDLE.clip_draw(int(self.frame) * 428, 0 , 428, 448, self.x, self.y)
            pass
        if self.state == 1:
            self.READY.clip_draw(int(self.frame) * 428, 0 , 428, 448, self.x, self.y)
            pass
        if self.state == 2:
            self.FIRE.clip_draw(int(self.frame) * 428, 0 , 428, 448, self.x, self.y)
            pass
        if self.state == 3:
            self.CHARGE.clip_draw(int(self.frame) * 428, 0 , 428, 448, self.x, self.y)
            pass
        if self.state == 4:
            self.DEAD.clip_draw(int(self.frame) * 428, 0 , 428, 448, self.x, self.y)
            pass
        pass
    pass

    def trace_player(self):
        kirby= game_world.get_player_layer()
        targetY = kirby.getPoint()[1]

        if targetY > self.y+10:
            self.y += RUN_SPEED_PPS * game_framework.frame_time
        else:
            self.y -= RUN_SPEED_PPS * game_framework.frame_time

        pass
    def shoot_fire(self):
        pass
    def rushing_body(self):
        pass


    def getPoint(self): return (self.x-14, self.y-32)
    def getRadius(self): return self.radius

    def getRect(self):
        return [(self.x-14-75,self.x-14+75,self.y-32-37,self.y-32+37),
                (self.x-14-37,self.x-14+37,self.y-32-80,self.y-32+70)]

    def getState(self): return self.state
    def getHP(self): return self.HP
    def getHurt(self, damage):
        self.HP-= damage

    def isDead(self):
        if self.HP > 0:
            return False
        else:
            return True
    def Kill(self): self.HP = 0

class kracko:
    image = None
    EYEimage = None
    def __init__(self):
        self.x, self.y = 1500,768//2
        self.maxHP, self.HP = 60, 60
        self.radius = 128
        self.frame = 0
        self.state = 0
        self.guarding = 1
        self.wait = 2
        self.count = 0
        self.bulletDir = 100
        self.speed = RUN_SPEED_PPS*2
        #self.build_behavior_tree()
        self.gause = None
        if kracko.image == None:
            kracko.image = load_image("image/boss/kracko/Kracko_Body.png")
            kracko.EYEimage =load_image("image/boss/kracko/Kracko_Eye.png")
        pass
    def Trace_Player_On_Top(self):
        kirby= game_world.get_player_layer()[0]
        targetY = kirby.getPoint()[1]

        if targetY > 512:
            self.x, self.y = 1224 , 512+128
            self.wait = 4
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def Trace_Player_On_Middle(self):
        kirby= game_world.get_player_layer()[0]
        targetY = kirby.getPoint()[1]

        if targetY > 256:
            self.x, self.y = 1224 , 256+128
            self.wait = 4
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def Trace_Player_On_Bottom(self):
        kirby= game_world.get_player_layer()[0]
        targetY = kirby.getPoint()[1]

        if targetY > 0:
            self.x, self.y = 1224 , 0+128
            self.wait = 4
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass


    def Battle_Resting(self):
            if self.x < 0:
                pass
            if self.wait < 0 :
                return BehaviorTree.SUCCESS
            return BehaviorTree.FAIL
            pass

    def Kracko_in_window(self):
            if self.x < 1024 + 564 and self.y < 768 + 128 and self.x > 0 - 564 and self.y > 0 - 128 :
                return True
            return False
            pass

    def build_behavior_tree(self):
        battle_rest_node = LeafNode("Battle Resting", self.Battle_Resting)
        upSide_node = LeafNode("Trace Player On Top", self.Trace_Player_On_Top)
        midSide_node = LeafNode("Trace Player On Middle", self.Trace_Player_On_Middle)
        downSide_node = LeafNode("Trace Player On Bottom", self.Trace_Player_On_Bottom)

        rest_node = SequenceNode("rest")
        rest_node.add_children(battle_rest_node,upSide_node,midSide_node,downSide_node)

        '''
        charge_upSide_node = SequenceNode("charge upSide")
        charge_upSide_node.add_child(upSide_node)

        charge_midSide_node = SequenceNode("charge midSide")
        charge_midSide_node.add_child(midSide_node)

        charge_downSide_node = SequenceNode("charge downSide")
        charge_downSide_node.add_child(downSide_node)
        '''

        rest_charge_node = SelectorNode("RestCharge")
        rest_charge_node.add_child(rest_node)
        self.bt = BehaviorTree(rest_charge_node)
        pass

    def update(self):
        if self.gause == None:
            self.gause = bossGause(self.maxHP)
        else:
            self.gause.update(self.HP)

        if self.HP > 0:
            #self.bt.run()
            kirby = game_world.get_player_layer()[0]
            target = kirby.getPoint()

            if self.wait>0:
                self.wait-=game_framework.frame_time
            else:
                self.x -= self.speed * game_framework.frame_time
                self.count -= game_framework.frame_time
                if self.Kracko_in_window():
                    if self.count < 0:
                        game_world.add_object(enemyBullet((self.x, self.y), (target[0], target[1] + 100)), 8)
                        game_world.add_object(enemyBullet((self.x, self.y), (target[0], target[1])), 8)
                        game_world.add_object(enemyBullet((self.x, self.y), (target[0], target[1] - 100)), 8)
                        self.count += 0.03

            self.frame = (self.frame +
                FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

            if self.x<-600:
                self.wait=1
                if target[1] > 512:
                    self.y = 512+128
                elif target[1] > 256:
                    self.y = 256+128
                elif target[1] > 0:
                    self.y = 0+128
                self.x = 1500


                #game_world.add_object(enemyBullet((self.x,self.y),(self.x,self.y+self.bulletDir)), 8)

            else:
                pass

        else:
            self.maxHP-=0.8
            self.image.opacify(self.maxHP/100)
            self.EYEimage.opacify(self.maxHP/100)
            #진동->렌더
            #이팩트
            #시간되면서 소멸
            self.getHurt(1)
            if self.maxHP<0:
                game_world.remove_object2(self, 5)

    def render(self):
        kirby = game_world.get_player_layer()[0]
        self.watch = getAngle((self.x,self.y),(kirby.getPoint()[0],kirby.getPoint()[1]))
        self.gause.render()
        self.image.clip_draw(int(self.frame) * 376, 0 , 376, 256, self.x, self.y)
        self.EYEimage.clip_composite_draw(0, 0 , 96, 96,-self.watch,'', self.x, self.y,96,96)
        draw_rectangle(*(self.getRect()[0][0],self.getRect()[0][2],self.getRect()[0][1],self.getRect()[0][3]))
        draw_rectangle(*(self.getRect()[1][0],self.getRect()[1][2],self.getRect()[1][1],self.getRect()[1][3]))


    def getPoint(self): return (self.x, self.y)
    def getRadius(self): return self.radius

    def getRect(self):
        return [(self.x-188,self.x+188,self.y-64,self.y+64),
                (self.x-94,self.x+94,self.y-128,self.y+128)]

    def getState(self) : return self.state
    def getHP(self) : return self.HP
    def getHurt(self, damage) :
        self.HP-= damage
        game_world.add_object(Smoke((self.x+random.randint(-188,188), self.y+random.randint(-128,128))), 10)
        game_world.add_object(Smoke((self.x+random.randint(-188,188), self.y+random.randint(-128,128))), 10)

    def isDead(self):
        if self.HP > 0:
            return False
        else:
            return True
    def Kill(self): self.HP = 0
    pass

class darkZero:
    pass