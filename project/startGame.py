from pico2d import *

import game_framework
import logo
import inGame

def WINSIZEX(): return 1024
def WINSIZEY(): return 768

open_canvas(WINSIZEX(),WINSIZEY(),sync=True)

game_framework.run(logo)

close_canvas()