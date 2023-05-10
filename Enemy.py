
from random import randint
import pygame
from Ship import Ship
from Fire import Fire
from Constants import Constants as C

ALL_SPACE_SHIPS = [C.RED_SPACE_SHIPS, C.BLUE_SPACE_SHIPS, C.YELLOW_SPACE_SHIPS]

class Enemy(Ship):

    def __init__(self, level, x, y, health=100):
        super().__init__(level, x, y, health)
        self.ship_image = ALL_SPACE_SHIPS[randint(0, 2)][level - 1]
        self.fire = Fire(level, level * 5, 0, 0)
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health
        self.speed = int(self.level * 1.2)
        self.moving_positions = []
        self.position_index = 0
        self.isUp = True

    def draw(self, window):
        self.draw_health(window)
        window.blit(self.ship_image, (self.x, self.y))
    
    def move(self):
        if self.level == 1 or self.level == 2:
            self.x -= self.speed
        elif self.level == 3 or self.level == 4:
            self.x -= self.speed
            if self.position_index == len(self.moving_positions):
                self.position_index = 0
                self.enhancedRandomizer()
            else:
                move_value = self.moving_positions[self.position_index]
                self.position_index += 1
                if not (self.y + move_value < 0) and not (self.y + move_value > C.HEIGHT - 100):
                    self.y += move_value if self.isUp else -move_value
        else: # level == 5
            self.x -= self.speed
            if self.position_index == len(self.moving_positions):
                self.position_index = 0
                self.enhancedRandomizer()
            else:
                move_value = self.moving_positions[self.position_index]
                self.position_index += 1
                if not (self.y + move_value < 0) and not (self.y + move_value > C.HEIGHT - 100):
                    self.y += -move_value if self.isUp else move_value

    def enhancedRandomizer(self):
        self.moving_positions.clear()
        self.setIsUp()
        randomRange = randint(1, 30)
        for i in range(0, randomRange):
            self.moving_positions.append(randint(1, self.level * 2))

        self.moving_positions.sort()
        growing_half = self.moving_positions[ : len(self.moving_positions)]

        self.moving_positions.sort(reverse=True)
        decreasing_half = self.moving_positions[ : len(self.moving_positions)]

        self.moving_positions.clear()
        self.moving_positions.extend(growing_half)
        self.moving_positions.extend(decreasing_half)

    def setIsUp(self):
        if self.y < 200:
            self.isUp = False
        elif self.y > C.HEIGHT - 200:
            self.isUp = True
        else:
            self.isUp = True if randint(0, 100) < 50 else False

    def is_outside(self):
        return (not (0 - self.mask.get_size()[0]<= self.x <= C.WIDTH)) or (not (-1 <= self.y <= C.HEIGHT))
    
    def is_passed(self):
        return not (0 - self.mask.get_size()[0]<= self.x <= C.WIDTH)
        
    def draw_health(self, window):
        pygame.draw.rect(window, C.RED, (self.x - abs((self.mask.get_size()[0] - self.max_health) / 2), self.y - 10, self.max_health, 6))
        pygame.draw.rect(window, C.GREEN, (self.x - abs((self.mask.get_size()[0] - self.max_health) / 2), self.y - 10, self.health, 6))

    def take_damage(self, damage):
        self.health -= damage
    
    def collide(self, obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

    def collision(self, obj):
        return self.collide(self, obj)