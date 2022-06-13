
import pygame
from Constants import Constants as C

FIRES = C.FIRES
WIDTH = C.WIDTH
HEIGHT = C.HEIGHT
VELOCITY = C.VELOCITY

class Fire:

    def __init__(self, level, damage, x, y):
        self.level = level
        self.damage = damage
        self.x = x
        self.y = y
        self.img = FIRES[level - 1]
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        self.move(VELOCITY)

    def move(self, vel):
        self.x += vel

    def collide(self, obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

    def collision(self, obj):
        return self.collide(self, obj)

    def is_outside(self):
        return (not (0 <= self.x <= WIDTH)) or (not (0 <= self.y <= HEIGHT))
        