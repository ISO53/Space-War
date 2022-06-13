
from Constants import Constants as C

FIRES = C.FIRES
WIDTH = C.WIDTH
HEIGHT = C.HEIGHT
VELOCITY = C.VELOCITY

EXPLOSIONS = C.EXPLOSIONS

class Explosion:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.exp_index = 0
        self.img_list = EXPLOSIONS

    def draw(self, window):
        if self.exp_index == 8 * 2:
            return False;
        else:
            window.blit(self.img_list[int(self.exp_index / 2)], (self.x, self.y))
            self.exp_index += 1
