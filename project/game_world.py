
# layer 0: Background Objects
# layer 1: player Objects
# layer 2: enemy Objects
# layer 3: item Objects
# layer 4: playerBullet Objects
# layer 5: Boom Objects
# layer 6: enemyBullet Objects

objects = [[],[],[],[],[],[],[]]

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

def intersectAtoB(objectA, AList, objectB, BList):
    distance = None
    for A in range(len(objects[AList])):
        for B in range(len(objects[BList])):
            distance = getDistance(objectA.getPoint(), objectB.getPoint())
            #object마다 object.getRadius()가 필요함
            hitRange = objectA.getRadius() + objectB.getRadius()

            if distance <= hitRange:
                if AList == 1:
                    # objects[AList].[BList]제거시발동함수
                    #함수명 activate()로 통일시킬것
                    #3아이템
                    if BList == 3:
                        if objectB.getItemNum() == 0:
                            objectA.getItemNum()
                            pass
                        elif objectB.getItemNum() == 1:
                            objectA.getItemNum()
                            pass
                        elif objectB.getItemNum() == 2:
                            objectA.setBoom(1)
                            pass
                    #2,6 적, 적총알
                    if BList == 2 or BList == 6:
                        #현재 보스포함 5종 있음
                        pass
                    pass
                    objects[BList].remove(objectB)
                else:
                    objects[AList].remove(objectA)
                    # objects[AList].[BList]제거시발동함수
                    objects[BList].remove(objectB)

                '''
                '''
    pass

def clear():
    for o in all_objects():
        del o
    objects.clear()

def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o
