from pico2d import *
import game_framework
import game_world

class HPblock():
    image = None
    def __init__(self):
        if HPblock.image == None:
            HPblock.image = load_image("image/UI/HP.png");
        pass

    def render(self, point):
        self.image.draw(point[0],point[1])
        pass
    pass



class kirbyHPUI():
    def __init__(self,HP=5):
        self.stratPoint = (50,738)
        self.maxHP,self.curHP = HP,HP
        self.blocks = []
        self.blocks = [HPblock() for i in range(HP)]
        pass

    def update(self,kirbyHP):
        if self.curHP > self.maxHP:
            self.curHP = self.maxHP
        pass

    def render(self):
        for i in range(self.curHP):
            for block in self.blocks:
                block.render((self.stratPoint[0]+i*15,self.stratPoint[1]))
            pass

    def getHurt(self): self.curHP -= 1
    pass


class Lifeblock():
    image = None
    def __init__(self):
        if Lifeblock.image == None:
            Lifeblock.image = load_image("image/UI/life.png");
        pass

    def render(self, point):
        self.image.draw(point[0],point[1])
        pass
    pass

class kirbyLifeUI():
    def __init__(self,Life = 2):
        self.stratPoint = (50,40)
        self.life = Life
        self.blocks = []
        self.blocks = [Lifeblock() for i in range(Life)]
        pass

    def update(self,kirbyLife):
        pass

    def render(self):
        for i in range(self.life):
            for block in self.blocks:
                block.render((self.stratPoint[0]+i*40,self.stratPoint[1]))
            pass

    def youDead(self): self.life -= 1
    pass


class Boomblock():
    image = None
    def __init__(self):
        if Boomblock.image == None:
            Boomblock.image = load_image("image/UI/UIBoom.png");
        pass

    def render(self, point):
        self.image.draw(point[0],point[1])
        pass
    pass

class kirbyBoomUI():
    def __init__(self,Boom = 2):
        self.stratPoint = (50,90)
        self.boom = Boom
        self.blocks = []
        self.blocks = [Boomblock() for i in range(Boom)]
        pass

    def update(self,kirbyBoom):
        self.boom = kirbyBoom
        pass

    def render(self):
        for i in range(self.boom):
            for block in self.blocks:
                block.render((self.stratPoint[0]+i*25,self.stratPoint[1]))
            pass

    def useBoom(self): self.boom -= 1
    pass

class Numbers():
    image = None
    def __init__(self):
        self.num = 0
        if Numbers.image == None:
            Numbers.image = load_image("image/UI/numbers.png");
        pass

    def update(self,num):
        self.num = num
        pass

    def render(self, point):
        self.image.clip_draw(self.num*24,0,24,28,point[0],point[1])
        pass
    pass

class ScoreBoard():
    def __init__(self):
        self.stratPoint = (1024-24,786-50)
        self.score = 0
        self.blocks = []
        self.blocks = [(Numbers(),i) for i in range(9)]
        pass

    def update(self,Score=1):
        self.score += game_framework.frame_time*10
        for block in self.blocks:
            num = self.score
            for j in range(block[1]):
                num = int(num/10)
            print(block[1])
            block[0].update(int(num%10))
        pass

    def render(self):
        for block in self.blocks:
            block[0].render((self.stratPoint[0]-block[1]*24,self.stratPoint[1]))
        pass

    def upScore(self,plus=100): self.score += plus
    pass