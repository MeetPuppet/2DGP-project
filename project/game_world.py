import random

from Items import Coin
from Items import PowerUp
from Items import BoomUp

# layer 0: Background Objects
# layer 1: player Objects
# layer 2: enemy Objects
# layer 3: item Objects
# layer 4: playerBullet Objects
# layer 5: Boom Objects
# layer 6: enemyBullet Objects
# layer 7: effect Objects

objects = [[],[],[],[],[],[],[],[]]

import math
def getDistance(startPoint, endPoint):
    Xdistance = startPoint[0] - endPoint[0]
    Ydistance = startPoint[1] - endPoint[1]
    return math.sqrt(Xdistance**2+Ydistance**2)

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


def remove_object2(o, num):
    if o in objects[num]:
        objects[num].remove(o)
        del o



def intersectRectToRect():
    for i in range(2):
        for bullet in objects[4]:
            A=bullet.getRect()[i]
            for enemy in objects[2]:
                B=enemy.getRect()[i]

                if enemy.isBoss() == False:
                    if (B[0]<A[0] and B[1]>A[0]) or (A[0]<B[0] and A[1]>B[0]):
                        if (B[2]<A[2] and B[3]>A[2])or (A[2]<B[2] and A[3]>B[2]):
                            enemy.getHurt(bullet.getDamage())
                            itemNum = random.randint(0,10)
                            summonItem(itemNum)
                            if bullet.getSize() < 2:
                                bullet.removeBullet()
                            objects[1][0].upScore()
                        elif (B[2]<A[3] and B[3]>A[3])or (A[2]<B[3] and A[3]>B[3]):
                            enemy.getHurt(bullet.getDamage())
                            itemNum = random.randint(0,10)
                            summonItem(itemNum)
                            if bullet.getSize() < 2:
                                bullet.removeBullet()
                            objects[1][0].upScore()
                    elif (B[0]<A[1] and B[1]>A[1]) or (A[0]<B[1] and A[1]>B[1]):
                        if (B[2]<A[2] and B[3]>A[2])or (A[2]<B[2] and A[3]>B[2]):
                            enemy.getHurt(bullet.getDamage())
                            itemNum = random.randint(0,10)
                            summonItem(itemNum)
                            if bullet.getSize() < 2:
                                bullet.removeBullet()
                            objects[1][0].upScore()
                        elif (B[2]<A[3] and B[3]>A[3])or (A[2]<B[3] and A[3]>B[3]):
                            enemy.getHurt(bullet.getDamage())
                            itemNum = random.randint(0,10)
                            summonItem(itemNum)
                            if bullet.getSize() < 2:
                                bullet.removeBullet()
                            objects[1][0].upScore()
                else:
                    if (B[0]<A[0] and B[1]>A[0]) or (A[0]<B[0] and A[1]>B[0]):
                        if (B[2]<A[2] and B[3]>A[2])or (A[2]<B[2] and A[3]>B[2]):
                            enemy.getHurt(bullet.getDamage())
                            bullet.removeBullet()
                            objects[1][0].upScore()
                        elif (B[2]<A[3] and B[3]>A[3])or (A[2]<B[3] and A[3]>B[3]):
                            enemy.getHurt(bullet.getDamage())
                            bullet.removeBullet()
                            objects[1][0].upScore()
                    elif (B[0]<A[1] and B[1]>A[1]) or (A[0]<B[1] and A[1]>B[1]):
                        if (B[2]<A[2] and B[3]>A[2])or (A[2]<B[2] and A[3]>B[2]):
                            enemy.getHurt(bullet.getDamage())
                            bullet.removeBullet()
                            objects[1][0].upScore()
                        elif (B[2]<A[3] and B[3]>A[3])or (A[2]<B[3] and A[3]>B[3]):
                            enemy.getHurt(bullet.getDamage())
                            bullet.removeBullet()
                            objects[1][0].upScore()

        for Ebullet in objects[6]:
            A=Ebullet.getRect()[i]
            for player in objects[1]:
                B=player.getRect()[i]
                if (B[0]<A[0] and B[1]>A[0]) or (A[0]<B[0] and A[1]>B[0]):
                    if (B[2]<A[2] and B[3]>A[2])or (A[2]<B[2] and A[3]>B[2]):
                        player.hit()
                        Ebullet.removeBullet()
                    elif (B[2]<A[3] and B[3]>A[3])or (A[2]<B[3] and A[3]>B[3]):
                        player.hit()
                        Ebullet.removeBullet()
                elif (B[0]<A[1] and B[1]>A[1]) or (A[0]<B[1] and A[1]>B[1]):
                    if (B[2]<A[2] and B[3]>A[2])or (A[2]<B[2] and A[3]>B[2]):
                        player.hit()
                        Ebullet.removeBullet()
                    elif (B[2]<A[3] and B[3]>A[3])or (A[2]<B[3] and A[3]>B[3]):
                        player.hit()
                        Ebullet.removeBullet()

        for Item in objects[3]:
            A=Item.getRect()[i]
            for player in objects[1]:
                B=player.getRect()[i]
                if (B[0]<A[0] and B[1]>A[0]) or (A[0]<B[0] and A[1]>B[0]):
                    if (B[2]<A[2] and B[3]>A[2])or (A[2]<B[2] and A[3]>B[2]):
                        itemPower(player,Item.getItemNum())
                        objects[3].remove(Item)
                    elif (B[2]<A[3] and B[3]>A[3])or (A[2]<B[3] and A[3]>B[3]):
                        itemPower(player,Item.getItemNum())
                        objects[3].remove(Item)
                elif (B[0]<A[1] and B[1]>A[1]) or (A[0]<B[1] and A[1]>B[1]):
                    if (B[2]<A[2] and B[3]>A[2])or (A[2]<B[2] and A[3]>B[2]):
                        itemPower(player,Item.getItemNum())
                        objects[3].remove(Item)
                    elif (B[2]<A[3] and B[3]>A[3])or (A[2]<B[3] and A[3]>B[3]):
                        itemPower(player,Item.getItemNum())
                        objects[3].remove(Item)

    pass

def intersectDistance():

    for i in range(2):
        for boom in objects[5]:
            for j in (2, 6):
                for enemy in objects[j]:
                    if j == 2 and enemy.isBoss() == True:
                        if getDistance(boom.getPoint(), enemy.getPoint()) < boom.getRadius() + enemy.getRadius():
                            boom.boomActivate()
                            enemy.getHurt(10)
                    elif j==6:
                        if getDistance(boom.getPoint(), enemy.getPoint()) < boom.getRadius() + enemy.getRadius():
                            boom.boomActivate()
                            enemy.removeBullet()
                    else:
                        if getDistance(boom.getPoint(), enemy.getPoint()) < boom.getRadius() + enemy.getRadius():
                            boom.boomActivate()
                            enemy.getHurt(1)

        for player in objects[1]:
            for j in (2, 6):
                for enemy in objects[j]:

                    if getDistance(player.getPoint(), enemy.getPoint()) < player.getRadius() + enemy.getRadius()+150:
                        player.onGrog()
                        if getDistance(player.getPoint(), enemy.getPoint()) < player.getRadius() + enemy.getRadius():
                            player.hit()
                    else:
                        if player.getHP() > 1:
                            player.offGrog()




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

def summonItem(num):
    if num == 0:
        add_object(Coin((1024//2, 768//2)), 3)
        pass
    elif num == 1:
        add_object(PowerUp((1024 // 2, 768 // 2)), 3)
        pass
    elif num == 2:
        add_object(BoomUp((1024 // 2, 768 // 2)), 3)
        pass

def clear():
    for o in all_objects():
        del o
    objects.clear()

def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o
