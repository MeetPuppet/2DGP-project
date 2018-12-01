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

def add_objects(l, layer):
    objects[layer] += l

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
    KirbyGrogMode()
    KirbyBulletCollision()
    BossCollision()
    MinionsCollision()
    EnemyBulletCollision()
    KirbyBoomCollision()
    ItemCollision()
    lazerIntersectRectToRect()
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

def KirbyGrogMode():
    for player in objects[1]:
        A = player.getPoint()
        for i in (4,5,8):
            for enemyObject in objects[i]:
                B=enemyObject.getPoint()
                if (A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2 <= (enemyObject.getRadius() + player.getRadius() + 150) ** 2:
                    player.onGrog()
                else:
                    player.offGrog()


def BossIntersectRectToRect():
    for RectNum in range(2):
        for boss in objects[5]:
            if boss.getHP() > 0:
                A=boss.getRect()[RectNum]
                for player in objects[1]:
                    for RectNum2 in range(2):
                        B=player.getRect()[RectNum2]
                        if (B[0] < A[0] and B[1] > A[0]) or (A[0] < B[0] and A[1] > B[0]):
                            if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                                player.Hit()
                            elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                                player.Hit()
                        elif (B[0] < A[1] and B[1] > A[1]) or (A[0] < B[1] and A[1] > B[1]):
                            if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                                player.Hit()
                            elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                                player.Hit()
    pass

def BossIntersectDistance():
    for boss in objects[5]:
        if boss.getHP() > 0:
            A=boss.getPoint()
            for player in objects[1]:
                B = player.getPoint()
                if (A[0]-B[0])**2+(A[1]-B[1])**2 <= (boss.getRadius()+player.getRadius())**2:
                    player.Hit()
    pass



def MinionsIntersectRectToRect():
    for RectNum in range(2):
        for enemy in objects[4]:
            A=enemy.getRect()[RectNum]
            for player in objects[1]:
                for RectNum2 in range(2):
                    B=player.getRect()[RectNum2]
                    if (B[0] < A[0] and B[1] > A[0]) or (A[0] < B[0] and A[1] > B[0]):
                        if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                            player.Hit()
                        elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                            player.Hit()
                    elif (B[0] < A[1] and B[1] > A[1]) or (A[0] < B[1] and A[1] > B[1]):
                        if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                            player.Hit()
                        elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                            player.Hit()
    pass

def MinionsIntersectDistance():
    for minion in objects[4]:
        A=minion.getPoint()
        for player in objects[1]:
            B=player.getPoint()
            if (A[0]-B[0])**2+(A[1]-B[1])**2 <= (minion.getRadius()+player.getRadius())**2:
                player.Hit()
    pass



def EnemyBulletIntersectRectToRect():
    for RectNum in range(2):
        for enemyBullet in objects[8]:
            A=enemyBullet.getRect()[RectNum]
            for player in objects[1]:
                for RectNum2 in range(2):
                    B=player.getRect()[RectNum2]
                    if (B[0] < A[0] and B[1] > A[0]) or (A[0] < B[0] and A[1] > B[0]):
                        if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                            player.Hit()
                            enemyBullet.removeBullet()
                        elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                            player.Hit()
                            enemyBullet.removeBullet()
                    elif (B[0] < A[1] and B[1] > A[1]) or (A[0] < B[1] and A[1] > B[1]):
                        if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                            player.Hit()
                            enemyBullet.removeBullet()
                        elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                            player.Hit()
                            enemyBullet.removeBullet()
    pass

def EnemyBulletIntersectDistance():
    for enemyBullet in objects[8]:
        A=enemyBullet.getPoint()
        for player in objects[1]:
            B=player.getPoint()
            if (A[0]-B[0])**2+(A[1]-B[1])**2 <= (enemyBullet.getRadius()+player.getRadius())**2:
                player.Hit()
    pass


def ItemIntersectRectToRect():
    for RectNum in range(2):
        for player in objects[1]:
            A=player.getRect()[RectNum]
            for Item in objects[7]:
                B=Item.getRect()[RectNum]
                if (B[0] < A[0] and B[1] > A[0]) or (A[0] < B[0] and A[1] > B[0]):
                    if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                        itemPower(player, Item.getItemNum())
                        objects[7].remove(Item)
                    elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                        itemPower(player, Item.getItemNum())
                        objects[7].remove(Item)
                elif (B[0] < A[1] and B[1] > A[1]) or (A[0] < B[1] and A[1] > B[1]):
                    if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                        itemPower(player, Item.getItemNum())
                        objects[7].remove(Item)
                    elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                        itemPower(player, Item.getItemNum())
                        objects[7].remove(Item)
    pass

def ItemIntersectDistance():
    pass



def KirbyBulletIntersectRectToRect():
    for RectNum in range(2):
        for enemy in objects[4]:
            A=enemy.getRect()[RectNum]
            for bullet in objects[3]:
                for RectNum2 in range(2):
                    B=bullet.getRect()[RectNum2]
                    if (B[0] < A[0] and B[1] > A[0]) or (A[0] < B[0] and A[1] > B[0]):
                        if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                            enemy.getHurt(bullet.getDamage())
                            bullet.removeBullet()
                            objects[1][0].upScore()
                        elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                            enemy.getHurt(bullet.getDamage())
                            bullet.removeBullet()
                            objects[1][0].upScore()
                    elif (B[0] < A[1] and B[1] > A[1]) or (A[0] < B[1] and A[1] > B[1]):
                        if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                            enemy.getHurt(bullet.getDamage())
                            bullet.removeBullet()
                            objects[1][0].upScore()
                        elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                            enemy.getHurt(bullet.getDamage())
                            bullet.removeBullet()
                            objects[1][0].upScore()
        for enemy in objects[5]:
            A=enemy.getRect()[RectNum]
            for bullet in objects[3]:
                for RectNum2 in range(2):
                    B=bullet.getRect()[RectNum2]
                    if (B[0] < A[0] and B[1] > A[0]) or (A[0] < B[0] and A[1] > B[0]):
                        if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                            enemy.getHurt(bullet.getDamage())
                            bullet.removeBullet()
                            objects[1][0].upScore()
                        elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                            enemy.getHurt(bullet.getDamage())
                            bullet.removeBullet()
                            objects[1][0].upScore()
                    elif (B[0] < A[1] and B[1] > A[1]) or (A[0] < B[1] and A[1] > B[1]):
                        if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                            enemy.getHurt(bullet.getDamage())
                            bullet.removeBullet()
                            objects[1][0].upScore()
                        elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                            enemy.getHurt(bullet.getDamage())
                            bullet.removeBullet()
                            objects[1][0].upScore()
    pass

def KirbyBulletIntersectDistance():
    pass



def KirbyBoomIntersectRectToRect():
    pass

def KirbyBoomIntersectDistance():
    for Boom in objects[6]:
        A=Boom.getPoint()

        for minion in objects[4]:
            M=minion.getPoint()
            if (A[0]-M[0])**2+(A[1]-M[1])**2 <= (Boom.getRadius()+minion.getRadius())**2:
                Boom.boomActivate()
                minion.getHurt(5)

        for boss in objects[5]:
            B=boss.getPoint()
            if (A[0]-B[0])**2+(A[1]-B[1])**2 <= (Boom.getRadius()+boss.getRadius())**2:
                Boom.boomActivate()
                boss.getHurt(5)

        for enemyBullet in objects[8]:
            EB=enemyBullet.getPoint()
            if (A[0]-EB[0])**2+(A[1]-EB[1])**2 <= (Boom.getRadius()+enemyBullet.getRadius())**2:
                Boom.boomActivate()
                enemyBullet.removeBullet()
    pass

def lazerIntersectRectToRect():
    for RectNum1 in range(2):
        for lazer in objects[9]:
            A=lazer.getRect()[RectNum1]
            for player in objects[1]:
                for RectNum2 in range(2):
                    B=player.getRect()[RectNum2]
                    if (B[0] < A[0] and B[1] > A[0]) or (A[0] < B[0] and A[1] > B[0]):
                        if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                            player.Hit()
                        elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                            player.Hit()
                    elif (B[0] < A[1] and B[1] > A[1]) or (A[0] < B[1] and A[1] > B[1]):
                        if (B[2] < A[2] and B[3] > A[2]) or (A[2] < B[2] and A[3] > B[2]):
                            player.Hit()
                        elif (B[2] < A[3] and B[3] > A[3]) or (A[2] < B[3] and A[3] > B[3]):
                            player.Hit()
    pass


def itemPower(o,num):
    if num == 0:
        o.upScore()
        pass
    elif num == 1:
        o.summonShooter()
        pass
    elif num == 2:
        o.setBoom()
        pass

def summonItem(point, num):
    if num == 0:
        add_object(Coin(point), 7)
        pass
    elif num == 1:
        add_object(PowerUp(point), 7)
        pass
    elif num == 2:
        add_object(BoomUp(point), 7)
        pass
    else:
        pass

def clear():
    for l in objects:
        l.clear()

def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

def get_player_layer():
    return objects[1]

def get_backGound():
    return objects[0][0]