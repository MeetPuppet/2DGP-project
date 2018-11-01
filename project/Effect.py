from pico2d import *

class effect:
    class status(enum.Enum):
        FORCE = 0
        SMOKE = 1
        COLLISION = 2
        DESTROY = 3
        BEAT = 4
    def __init__(self):
        pass
    def update(self):
        pass
    def render(self):
        pass
    pass