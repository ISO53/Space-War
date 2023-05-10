
import pygame
import os

pygame.init()
infoObject = pygame.display.Info()

class Constants:
    WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
    VELOCITY = 40

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("SPACE WAR")

    BACKGROUND1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "BACKGROUND.png")), (WIDTH, HEIGHT))
    BACKGROUND2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "BACKGROUND.png")), (WIDTH, HEIGHT))

    BACKGROUND1_ALPHA = pygame.transform.scale(pygame.image.load(os.path.join("images", "BACKGROUND2.png")).convert(), (WIDTH, HEIGHT))
    BACKGROUND2_ALPHA = pygame.transform.scale(pygame.image.load(os.path.join("images", "BACKGROUND2.png")).convert(), (WIDTH, HEIGHT))
    BACKGROUND1_ALPHA.set_alpha(75)
    BACKGROUND2_ALPHA.set_alpha(75)

    EXPLOSIONS = []
    for i in range(1, 9):
        EXPLOSIONS.append(pygame.image.load(os.path.join("images\\EXPLOSION", "EXP_" + str(i) + ".png")))
    
    RED_SPACE_SHIPS = []
    for i in range(1, 6):
        RED_SPACE_SHIPS.append(pygame.image.load(os.path.join("images\\RED_SHIP", "RED_SHIP_" + str(i) + ".png")))

    BLUE_SPACE_SHIPS = []
    for i in range(1, 6):
        BLUE_SPACE_SHIPS.append(pygame.image.load(os.path.join("images\\BLUE_SHIP", "BLUE_SHIP_" + str(i) + ".png")))

    YELLOW_SPACE_SHIPS = []
    for i in range(1, 6):
        YELLOW_SPACE_SHIPS.append(pygame.image.load(os.path.join("images\\YELLOW_SHIP", "YELLOW_SHIP_" + str(i) + ".png")))

    MAIN_SPACE_SHIPS = []
    for i in range(1, 6):
        MAIN_SPACE_SHIPS.append(pygame.image.load(os.path.join("images\\MAIN_SHIP", "MAIN_SHIP_" + str(i) + ".png")))
    
    FIRES = []
    for i in range(1, 6):
        FIRES.append(pygame.image.load(os.path.join("images\\FIRE", "FIRE_" + str(i) + ".png")))
    
    LASER_SOUND = pygame.mixer.Sound("sounds\\laser.wav")
    EXPLOSION_SOUND = pygame.mixer.Sound("sounds\\explosion.wav")
    BACKGROUND_SOUND = pygame.mixer.music.load("sounds\\game_theme.mp3")
    pygame.mixer.music.set_volume(0.5)

    