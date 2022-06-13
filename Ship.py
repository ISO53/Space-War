
from Constants import Constants as C

class Ship:
    def __init__(self, level, x, y, health=100):
        self.level = level
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.fire_image = None
        self.fires = []
        self.cool_down_counter = 0;
    
    def draw(self, window):
        window.blit(self.ship_image, (self.x, self.y))
    
    def get_width(self):
        return self.ship_image.get_width()
    
    def get_heigth(self):
        return self.ship_image.get_height()
    
    def is_outside(self):
        return (not (0 <= self.x <= C.WIDTH)) or (not (0 <= self.y <= C.HEIGHT))