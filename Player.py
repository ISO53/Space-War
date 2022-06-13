
from operator import le
from Fire import Fire
from Ship import Ship
from Constants import Constants as C
import pygame

MAIN_SPACE_SHIPS = C.MAIN_SPACE_SHIPS


class Player(Ship):

    def __init__(self, level, x, y, health=600):
        super().__init__(level, x, y, health)
        self.ship_image = MAIN_SPACE_SHIPS[level - 1]
        self.fire_obj = Fire(level, level * 30, self.x, self.y)
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health
        self.fire_cooldown = 20
        self.kill_count = 0
    
    def is_outside(self):
        return (not (0 <= self.x <= C.WIDTH)) or (not (0 <= self.y <= C.HEIGHT))

    def new_fire(self):
        return Fire(self.level, self.level * 5, self.x + self.mask.get_size()[0], self.y + self.mask.get_size()[1] / 2)

    def set_coordinations(self, x, y):
        self.x = x
        self.y = y
    
    def draw_health(self, window):
        pygame.draw.rect(window, C.RED, (self.x - abs((self.mask.get_size()[0] - self.max_health / 6) / 2), self.y - 10, self.max_health / 6, 6))
        pygame.draw.rect(window, C.GREEN, (self.x - abs((self.mask.get_size()[0] - self.max_health / 6) / 2), self.y - 10, self.health / 6, 6))
    
    def enemy_killed(self):
        self.kill_count += 1
        if self.kill_count % 3 == 0 and self.level != 5:
            self.level += 1
            self.ship_image = MAIN_SPACE_SHIPS[self.level - 1]
            self.mask = pygame.mask.from_surface(self.ship_image)
            self.health = self.max_health

    def take_damage(self):
        self.health -=1