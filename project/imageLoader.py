import pico2d

class setbataImages():
    IDLE = None
    READY = None
    FIRE = None
    CHARGE = None
    DEAD = None
    def __init__(self):
        if setbataImages.IDLE == None:
            self.IDLE = pico2d.load_image("image/boss/batafireIDLE.png")
    def update(self):
        pass
    def render(self):
        self.a=0
    def getBatafireIDLE(self): return id(self.IDLE)
    pass
'''
        if setbataImages.READY == None:
            self.READY = pico2d.load_image("image/boss/batafireReady.png")
        if setbataImages.FIRE == None:
            self.FIRE = pico2d.load_image("image/boss/batafireFire.png")
        if setbataImages.CHARGE == None:
            self.CHARGE = pico2d.load_image("image/boss/batafireCharge.png")
        if setbataImages.DEAD == None:
            self.DEAD = pico2d.load_image("image/boss/batafireDead.png")
'''


bataFire = setbataImages()

def getBossImage(): return bataFire.getBatafireIDLE()