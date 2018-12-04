from pico2d import *
import game_world
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import random
import rankTable


from UI import bossGause
from enemyBullets import Fireball, enemyBullet, getAngle, DarkStar
from minions import miniBata
from Effect import Beat,Smoke, chargeSpark, readyBurn
import inGame

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
    fireSound = None
    def __init__(self):
        if Batafire.fireSound == None:
            Batafire.fireSound = load_wav('sound/bataFire/song586.wav')
        self.x, self.y = 1500,768//2
        self.maxHP, self.HP = 100, 100
        self.radius = 90
        self.frame = 0
        self.state = 0
        self.guarding = 0.1
        self.wait = 10
        self.backMove = False
        self.UpMove = False
        self.count = 0
        self.falling = RUN_SPEED_PPS
        self.gause = None
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
        if self.guarding > 0:
            self.guarding-=game_framework.frame_time
        if self.gause == None:
            self.gause = bossGause(self.maxHP)
        else:
            self.gause.update(self.HP)

        if self.HP <= 0: self.state = 4

        kirby= game_world.get_player_layer()[0]
        target = kirby.getPoint()

        if self.state == 0:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10

            if self.backMove == True:
                self.x+=RUN_SPEED_PPS*game_framework.frame_time
            else:
                self.x-=RUN_SPEED_PPS*game_framework.frame_time
            if target[1] > self.y+20:
                self.y+=RUN_SPEED_PPS*game_framework.frame_time/2
            elif target[1] < self.y-20:
                self.y-=RUN_SPEED_PPS*game_framework.frame_time/2

            if self.x < 612:
                self.backMove = True
            elif self.x > 974:
                self.backMove = False

            self.wait -= game_framework.frame_time
            if self.wait < 0:
                self.frame = 0
                self.state = 1
            pass

        elif self.state == 1:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            if int(self.frame) == 3:
                for i in range(3): game_world.add_object(miniBata((1300,random.randint(100,668))),2)
                if target[0] < 200:
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
                Batafire.fireSound.play()
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
                inGame.setStageNum(1)
                game_world.remove_object2(self,5)

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
        #draw_rectangle(*(self.getRect()[0][0], self.getRect()[0][2], self.getRect()[0][1], self.getRect()[0][3]))
        #draw_rectangle(*(self.getRect()[1][0], self.getRect()[1][2], self.getRect()[1][1], self.getRect()[1][3]))

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


    def getPoint(self): return (self.x-10, self.y-60)
    def getRadius(self): return self.radius

    def getRect(self):
        return [(self.x-10-80,self.x-10+80,self.y-40-60,self.y+40-60),
                (self.x-10-30,self.x-10+30,self.y-80-60,self.y+80-60)]

    def getState(self): return self.state
    def getHP(self): return self.HP
    def getHurt(self, damage):
        if self.guarding < 0:
            self.guarding = 0.1
            self.HP-= damage
            kirby= game_world.get_player_layer()[0]
            target = kirby.getPoint()
            explo = random.randint(0,10)
            if explo == 0:
                game_world.add_object(Fireball((self.x - 100, self.y - 100), target), 8)


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
        self.attackMode = 0
        self.bulletDir = 100
        self.wayRight = False
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
        if self.guarding > 0:
            self.guarding-=game_framework.frame_time
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
                if self.wayRight == False:
                    self.x -= self.speed * game_framework.frame_time
                else:
                    self.x += self.speed * game_framework.frame_time

                self.count -= game_framework.frame_time
                if self.Kracko_in_window():
                    if self.count < 0:
                        if self.attackMode == 0:
                            game_world.add_object(enemyBullet((self.x, self.y), (target[0], target[1] + 100)), 8)
                            game_world.add_object(enemyBullet((self.x, self.y), (target[0], target[1])), 8)
                            game_world.add_object(enemyBullet((self.x, self.y), (target[0], target[1] - 100)), 8)
                        self.count += 0.4

            self.frame = (self.frame +
                FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

            if self.x<-600 and self.wayRight == False:
                self.wait=1
                if target[1] > 512:
                    self.y = 512+128
                elif target[1] > 256:
                    self.y = 256+128
                elif target[1] > 0:
                    self.y = 0+128
                self.wayRight = True
                self.makeSpark()

            elif self.x > 1024+600 and self.wayRight == True:
                self.wait=1
                if target[1] > 512:
                    self.y = 512+128
                elif target[1] > 256:
                    self.y = 256+128
                elif target[1] > 0:
                    self.y = 0+128
                self.wayRight = False
                self.makeSpark()
        else:
            self.maxHP-=0.8
            self.image.opacify(self.maxHP/100)
            self.EYEimage.opacify(self.maxHP/100)
            self.getHurt(1)
            if self.maxHP<0:
                    inGame.setStageNum(2)
                    game_world.remove_object2(self,5)

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


    def makeSpark(self):
        kirby = game_world.get_player_layer()[0]
        target = kirby.getPoint()
        game_world.add_object(chargeSpark(target), 10)
        game_world.add_object(chargeSpark((random.randint(100,900),random.randint(50,700))), 10)
        game_world.add_object(chargeSpark((random.randint(100,900),random.randint(50,700))), 10)
        game_world.add_object(chargeSpark((random.randint(100,900),random.randint(50,700))), 10)
        game_world.add_object(chargeSpark((random.randint(100,900),random.randint(50,700))), 10)

    def getState(self) : return self.state
    def getHP(self) :
        HP = self.HP
        return HP
    def getHurt(self, damage) :
        if self.guarding < 0:
            self.guarding = 0.1
            self.HP-= damage
            game_world.add_object(Smoke((self.x+random.randint(-188,188), self.y+random.randint(-128,128))), 10)

    def isDead(self):
        if self.HP > 0:
            return False
        else:
            return True
    def Kill(self): self.HP = 0
    pass

class darkZero:
    bodyImage = None
    eyeImage = None
    sound = None
    def __init__(self):
        if darkZero.sound == None:
            darkZero.sound = load_wav("sound/darkZero/summoning.wav")
        self.sound.set_volume(64)
        self.x, self.y = 1024+500,768//2
        self.maxHP, self.HP = 200, 200
        self.radius = 300
        self.frame = 0
        self.eyeFrame = 0
        self.guarding = 1
        self.intro = True
        self.wait = 3
        self.count = 1
        self.speed = RUN_SPEED_PPS/2
        self.gause = None
        if darkZero.bodyImage == None:
            darkZero.bodyImage = load_image("image/boss/darkZero/darkZero_body.png")
            darkZero.eyeImage = load_image("image/boss/darkZero/darkZero_eye.png")

        pass
    def update(self):
        if self.guarding > 0 and self.intro == False:
            self.guarding-=game_framework.frame_time
        if self.gause == None:
            self.gause = bossGause(self.maxHP)
        else:
            self.gause.update(self.HP)

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        if self.intro == True:
            self.x -= self.speed * game_framework.frame_time
            if self.x < 1024:
                self.eyeFrame = (self.eyeFrame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
                if int(self.eyeFrame)==1:self.sound.play()
                if int(self.eyeFrame) == 18:
                    self.intro = False
        else:
            if self.HP > 0:
                self.count -= game_framework.frame_time
                self.wait -= game_framework.frame_time
                if self.count < 0:
                    game_world.add_object(DarkStar(), 8)
                    self.count += 1
                if self.wait < 0:
                    self.wait += 4
                    if random.randint(0,1) == 0:
                        self.makeSpark()
                    else:
                        self.makeFireWall()
            else:
                self.maxHP-=1
                self.bodyImage.opacify(self.maxHP/200)
                self.eyeImage.opacify(self.maxHP/200)
                game_world.add_object(Beat((self.x+random.randint(-350,350), self.y+random.randint(-350,350))), 10)
                game_world.add_object(Smoke((self.x+random.randint(-350,350), self.y+random.randint(-350,350))), 10)
                if self.maxHP<=0:

                    game_world.remove_object2(self,5)
                    score = int(game_world.get_player_layer()[0].getScore())
                    try:
                        with open('data.json', 'r') as f:
                            data_list = json.load(f)
                        for j in range(5):
                            for i in range(5):
                                if data_list[i]["score"] <= score:
                                    data_list[i]["score"], score = score, data_list[i]["score"]
                        f.close()
                    except:
                        data_list = [{"rank": 1, "score": 1000000}, {"rank": 2, "score": 50000},
                                     {"rank": 3, "score": 30000}, {"rank": 4, "score": 10000},
                                     {"rank": 5, "score": 5000}]
                        for j in range(5):
                            for i in range(5):
                                if data_list[i]["score"] <= score:
                                    data_list[i]["score"], score = score, data_list[i]["score"]
                    with open('data.json', 'w') as f:
                        json.dump(data_list, f)

                    game_framework.change_state(rankTable)


            pass


            pass
        pass
    def render(self):
        self.gause.render()
        self.bodyImage.clip_draw(int(self.frame) * 585, 0 , 585, 702, self.x, self.y)
        self.eyeImage.clip_draw(int(self.eyeFrame) * 225, 0 , 225, 225, self.x-30, self.y-80)
        draw_rectangle(*(self.getRect()[0][0],self.getRect()[0][2],self.getRect()[0][1],self.getRect()[0][3]))
        draw_rectangle(*(self.getRect()[1][0],self.getRect()[1][2],self.getRect()[1][1],self.getRect()[1][3]))


        pass
    pass

    def makeSpark(self):
        kirby = game_world.get_player_layer()[0]
        target = kirby.getPoint()
        game_world.add_object(chargeSpark(target), 10)
        game_world.add_object(chargeSpark((random.randint(100,900),random.randint(50,700))), 10)
        game_world.add_object(chargeSpark((random.randint(100,900),random.randint(50,700))), 10)
        game_world.add_object(chargeSpark((random.randint(100,900),random.randint(50,700))), 10)
        game_world.add_object(chargeSpark((random.randint(100,900),random.randint(50,700))), 10)

    def makeFireWall(self):
        game_world.add_object(readyBurn(), 10)



    def getPoint(self): return (self.x, self.y-80)
    def getRadius(self): return self.radius

    def getRect(self):
        return [(self.x-243,self.x+243,self.y-80-150,self.y-80+150),
                (self.x-150,self.x+150,self.y-80-300,self.y-80+300)]

    def getHP(self): return self.HP
    def getHurt(self, damage):
        if self.guarding < 0:
            self.guarding = 0.1
            self.HP-= damage


    def isDead(self):
        if self.HP > 0:
            return False
        else:
            return True
    def Kill(self): self.HP = 0
    pass