
import pygame
import random

from Constants import Constants as C
from Player import Player
from Enemy import Enemy
from Fire import Fire
from Explosion import Explosion

pygame.font.init()
pygame.init()

# Window settings
WIDTH = C.WIDTH
HEIGHT = C.HEIGHT
WIN = C.WIN

# Load images
BACKGROUND1 = C.BACKGROUND1
BACKGROUND2 = C.BACKGROUND2
BACKGROUND1_ALPHA = C.BACKGROUND1_ALPHA
BACKGROUND2_ALPHA = C.BACKGROUND2_ALPHA

# Load sound effects
LASER_SOUND = C.LASER_SOUND
LASER_SOUND.set_volume(0.4)
EXPLOSION_SOUND = C.EXPLOSION_SOUND
EXPLOSION_SOUND.set_volume(1.0)
GAME_THEME = C.BACKGROUND_SOUND

# Variables
run = True
is_game_started = False
is_game_over = False
is_game_paused = False
lives = 3
fire_cooldown = 5
BG_ROLL = 0
BG_ROLL_2 = 0
BG_ROLLING_SPEED = 1 * 3
COOLDOWN = 240
FPS = 240
main_font = pygame.font.SysFont("century gothic", 50)
game_over_font = pygame.font.SysFont("century gothic", 150)
game_start_font = pygame.font.SysFont("century gothic", 100)
pause_font = pygame.font.SysFont("century gothic", 20)
clock = pygame.time.Clock()
player_velocity = 1 * 2 + 5
drawables = []
player = Player(1, 50, HEIGHT / 2)
drawables.append(player)

# Start the music
pygame.mixer.music.play(-1)

def redraw_window():
    WIN.blit(BACKGROUND1, (BG_ROLL, 0))
    WIN.blit(BACKGROUND2, (WIDTH + BG_ROLL, 0))
    WIN.blit(BACKGROUND1_ALPHA, (BG_ROLL_2 / 1.5, 0))
    WIN.blit(BACKGROUND2_ALPHA, (WIDTH + BG_ROLL_2 / 1.5, 0))

    # Draw text
    lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
    level_label = main_font.render(f"Level: {player.level}", 1, (255, 255, 255))
    kill_count_label = main_font.render(f"Total Kill: {player.kill_count}", 1, (255, 255, 255))
    pause_label = pause_font.render("Press P for pause", 1, (255, 255, 255))
    paused_label = game_over_font.render("PAUSED", 1, (255, 255, 255))

    WIN.blit(lives_label, (10, 10))
    WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
    WIN.blit(kill_count_label, (250, 10))
    if not is_game_paused:
        WIN.blit(pause_label, (10, HEIGHT - 80))
    else:
        WIN.blit(paused_label, ((WIDTH - paused_label.get_width()) / 2, (HEIGHT - paused_label.get_height()) / 2))

def paint_drawables():
    global drawables
    global player
    for drawable in drawables:

        if isinstance(drawable, Fire):
            if drawable.is_outside():
                drawables.remove(drawable)
                continue
            else:
                drawable.draw(WIN)

                for drawable2 in drawables:
                    if isinstance(drawable2, Enemy) and drawable.collision(drawable2):
                        try:
                            drawables.remove(drawable)  # removes fire
                        except ValueError:
                            ignore = 0  # ignore

                        # enemy takes damage
                        drawable2.take_damage(drawable.damage)
                        if drawable2.health < 0:
                            exp = Explosion(drawable2.x, drawable2.y)
                            drawables.append(exp)
                            drawables.remove(drawable2)
                            player.enemy_killed()

        if (isinstance(drawable, Enemy)):
            global lives
            if drawable.is_passed():
                lives -= 1
                drawables.remove(drawable)
                if lives == 0:
                    game_over()
            else:
                drawable.draw(WIN)
                if drawable.collision(player):  
                    player.take_damage()
                    drawable.take_damage(1)
                    if player.health <= 0:
                        game_over()
                    elif drawable.health <= 0:
                        exp2 = Explosion(drawable.x, drawable.y)
                        drawables.append(exp2)
                        drawables.remove(drawable)
                        player.enemy_killed()
                else:
                    drawable.move()

        if (isinstance(drawable, Explosion)):
            EXPLOSION_SOUND.play()
            if drawable.draw(WIN) == False:
                drawables.remove(drawable)

        if isinstance(drawable, Player):
            drawable.draw(WIN)
            drawable.draw_health(WIN)
            drawable.set_coordinations(drawable.x, drawable.y)

def display_update():
    pygame.display.update()

def spawn_enemies():
    if COOLDOWN % (240 / player.level) == 0:
        enemy = Enemy(player.level, WIDTH - 200, random.randint(0, HEIGHT - 200))
        enemy.enhancedRandomizer()
        drawables.append(enemy)

def game_over():
    global is_game_over
    is_game_over = True
    drawables.clear()
    redraw_window()
    paint_drawables()

def new_game():
    global is_game_over
    global is_game_started
    global lives
    lives = 3
    player.level = 1
    player.health = player.max_health
    drawables.append(player)
    is_game_over = False
    is_game_started = True
    player.ship_image = C.MAIN_SPACE_SHIPS[player.level - 1]
    player.mask = pygame.mask.from_surface(player.ship_image)
    player.set_coordinations(100, HEIGHT / 2)
    player.kill_count = 0

while run:
    clock.tick(FPS)

    if is_game_paused:
        redraw_window()
    elif is_game_over:
        # game over screen
        redraw_window()
        game_over_label = game_over_font.render("GAME OVER", 1, (255, 255, 255))
        WIN.blit(game_over_label, ((WIDTH - game_over_label.get_width()) / 2, (HEIGHT - game_over_label.get_height()) / 2 - 100))
        score_label = game_over_font.render(f"Your Score: {player.kill_count}", 1, (255, 255, 255))
        WIN.blit(score_label, ((WIDTH - score_label.get_width()) / 2, (HEIGHT - score_label.get_height()) / 2 + 50))
        new_game_label = main_font.render("Press ENTER for new game", 1, (255, 255, 255))
        WIN.blit(new_game_label, ((WIDTH - new_game_label.get_width()) / 2, (HEIGHT - new_game_label.get_height()) / 2 + 250))
    elif not is_game_started:
        # game start screen
        redraw_window()
        game_start_label = game_start_font.render("WELCOME TO SPACE WAR", 1, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        WIN.blit(game_start_label, ((WIDTH - game_start_label.get_width()) / 2, (HEIGHT - game_start_label.get_height()) / 2 - 100))
        new_game_label = main_font.render("Press ENTER for new game", 1, (255, 255, 255))
        WIN.blit(new_game_label, ((WIDTH - new_game_label.get_width()) / 2, (HEIGHT - new_game_label.get_height()) / 2 + 150))
    else:
        redraw_window()
        paint_drawables()
        spawn_enemies()

    display_update()

    BG_ROLLING_SPEED = player.level * 3
    player_velocity = player.level * 2 + 5

    COOLDOWN = 240 if COOLDOWN == 1 else (COOLDOWN - 1)

    if not is_game_paused:
        BG_ROLL = (BG_ROLL - BG_ROLLING_SPEED) if (BG_ROLL - BG_ROLLING_SPEED) > - WIDTH else 0
        BG_ROLL_2 = (BG_ROLL_2 - BG_ROLLING_SPEED) if (BG_ROLL_2 - BG_ROLLING_SPEED) > - WIDTH * 1.5 else 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        quit()
    if keys[pygame.K_p]:        # pause
        if is_game_started:
            if is_game_paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            is_game_paused = not is_game_paused
    if keys[pygame.K_w]:        # up
        player.y = -player.mask.get_size()[1] / 2 if player.y - player_velocity < -player.mask.get_size()[1] / 2 else player.y - player_velocity
    if keys[pygame.K_a]:        # left
        player.x = 0 if player.x - player_velocity < 0 else player.x - player_velocity
    if keys[pygame.K_s]:        # down
        player.y = HEIGHT - player.get_heigth() if player.y + player_velocity > HEIGHT - player.get_heigth() else player.y + player_velocity
    if keys[pygame.K_d]:        # right
        player.x = WIDTH - player.get_width() if player.x + player_velocity > WIDTH - player.get_width() else player.x + player_velocity
    if keys[pygame.K_SPACE]:    # fire
        if COOLDOWN % fire_cooldown == 0:
            drawables.append(player.new_fire())
            LASER_SOUND.play()
    if keys[pygame.K_RETURN]:    # new game
        if is_game_over or (not is_game_started):
            new_game()
