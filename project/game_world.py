import random

from Items import Coin
from Items import PowerUp
from Items import BoomUp

#if i could use this, it would realy usefull
#BackGround, Player, Enemies, Items, playerBullets, Boom, enemyBullets, Effect = range(8)


# layer 0: Background Objects
# layer 1: player Objects
# layer 2: suporter Objects
# layer 3: playerBullet Objects        (self->enemys)
# layer 4: minion Objects              (self->Kirby)
# layer 5: Boss Objects                (self->Kirby)
# layer 6: Boom Objects                (self->enemys)
# layer 7: item Objects                (self->Kirby)
# layer 8: enemyBullet Objects         (self->Kirby)
# layer 9: enemyUnstoppable Lager Objects (self->Kirby)
# layer 10: effect Objects

objects = [[],[],[],[],[],[],[],[],[],[],[]]

import math
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
def getDistance(startPoint, endPoint):
    Xdistance = (startPoint[0] - endPoint[0])**2
    Ydistance = (startPoint[1] - endPoint[1])**2
    return math.sqrt(Xdistance+Ydistance)

def getAngle(startPoint, endPoint):

    Xdistance = endPoint[0] - startPoint[0]
    Ydistance = endPoint[1] - startPoint[1]
    distance = math.sqrt(Xdistance ** 2 + Ydistance ** 2)

    angle = math.cos(Xdistance / distance)

    if endPoint[1] > startPoint[1] :
        angle = (3.141592*2) - angle
        if angle > (3.141592*2):
            angle -= (3.141592*2)

    return angle

    pass


def add_object(o, layer):
    objects[layer].append(o)

def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o
            break

def remove_object2(o, num):
    if o in objects[num]:
        objects[num].remove(o)
        del o


def CommunicateObjects():
    KirbyBulletCollision()
    BossCollision()
    MinionsCollision()
    EnemyBulletCollision()
    KirbyBoomCollision()
    ItemCollision()
    pass

def KirbyBoomCollision():
    KirbyBoomIntersectDistance()
    KirbyBoomIntersectRectToRect()
    pass

def KirbyBulletCollision():
    KirbyBulletIntersectRectToRect()
    KirbyBulletIntersectDistance()
    pass
def EnemyBulletCollision():
    EnemyBulletIntersectRectToRect()
    EnemyBulletIntersectDistance()
    pass

def BossCollision():
    BossIntersectDistance()
    BossIntersectRectToRect()
    pass
def MinionsCollision():
    MinionsIntersectDistance()
    MinionsIntersectRectToRect()
    pass
def ItemCollision():
    ItemIntersectRectToRect()
    ItemIntersectDistance()
    pass

def BossIntersectRectToRect():

    pass

def BossIntersectDistance():
    for boss in objects[5]:
        A=boss.getPoint()
        for player in objects[1]:
            B=player.getPoint()
            if (A[0]-B[0])**2+(A[1]-B[1])**2 <= boss.getRadius()**2:
                player.Hit()
                #여기부터

    pass



def MinionsIntersectRectToRect():
    pass

def MinionsIntersectDistance():
    pass



def EnemyBulletIntersectRectToRect():
    pass

def EnemyBulletIntersectDistance():
    pass


def ItemIntersectRectToRect():
    pass

def ItemIntersectDistance():
    pass



def KirbyBulletIntersectRectToRect():
    for RectNum in range(2):
        for boss in objects[5]:
            A=boss.getRect()[RectNum]
            for bullet in objects[3]:
                B=bullet.getRect()[RectNum]
                if (B[0] < A[0] and B[1] > A[0]) or (A[0] < B[0] and A[1] > B[0]):
                    if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                        boss.getHurt(bullet.getDamage())
                        bullet.removeBullet()
                        objects[1][0].upScore()
                    elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                        boss.getHurt(bullet.getDamage())
                        bullet.removeBullet()
                        objects[1][0].upScore()
                elif (B[0] < A[1] and B[1] > A[1]) or (A[0] < B[1] and A[1] > B[1]):
                    if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                        boss.getHurt(bullet.getDamage())
                        bullet.removeBullet()
                        objects[1][0].upScore()
                    elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                        boss.getHurt(bullet.getDamage())
                        bullet.removeBullet()
                        objects[1][0].upScore()
    pass

def KirbyBulletIntersectDistance():
    pass



def KirbyBoomIntersectRectToRect():
    pass

def KirbyBoomIntersectDistance():
    pass


def itemPower(o,num):
    if num == 0:
        o.upScore()
        pass
    elif num == 1:
        #먹어지기만 함
        pass
    elif num == 2:
        o.setBoom()
        pass

def summonItem(point, num):
    if num == 0:
        add_object(Coin(point), 3)
        pass
    elif num == 1:
        add_object(PowerUp(point), 3)
        pass
    elif num == 2:
        add_object(BoomUp(point), 3)
        pass
    else:
        pass

def clear():
    for o in all_objects():
        del o
    objects.clear()

def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

def get_player_layer():
    return objects[1]
