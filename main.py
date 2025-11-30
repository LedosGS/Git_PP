import sys
import pygame
import math
# from constants import *
# from Entity import *
from Dino import *
from Button import *
from Ground import *
from Cactus import *

dev_version = False
pygame.init()
screen = pygame.display.set_mode(Resolutions.MAX, pygame.SRCALPHA, pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Dino")
clock = pygame.time.Clock()
info = pygame.display.Info()
color = WHITE
font = pygame.font.Font(None, screen.get_height() // 20)

cactus_2: Cactus
cactus: Cactus_group
dino: Dino
ground: Ground

current_state = GameState.MENU
ground_height = screen.get_height() * 0.85
last_time = pygame.time.get_ticks()

dino_step = 1
dino_state = 0
dino_seat = 0
last_update = pygame.time.get_ticks()
anim_speed = 100

jump_height = screen.get_height() / 3
on_ground = True
is_jumping = False
dino_start_position_y = 0
jump_duration = 0
jump_time = 0
jump_force = 1.0

space_hold_time = 0
is_space_pressed = False
max_hold_time = 0.5

FPS_limit = 75
base_speed = 400
current_speed = base_speed
max_speed = 2400
acceleration_rate = 12  # пикселей/секунду²
game_time = 0
score = 0.0

button_resize = Button(screen, screen.get_width() / 20, screen.get_width() / 20, screen.get_width() / 20,
                       screen.get_width() / 20, "MI")


def spawn_all_entitys():
    global dino
    global dino_start_position_y
    global jump_height
    global ground
    global cactus
    global screen

    dino = Dino(screen, 'dino',
                  (0, ground_height),
                  screen.get_width() // 10)

    ground = Ground(screen, 'road',
                    (0, ground_height),
                    screen.get_width())
    cactus = Cactus_group(screen, 'cactus',
                    (screen.get_width() / 2, screen.get_height() / 2),
                    width=(screen.get_width() // 10))

    dino_start_position_y = dino.position[1]
    jump_height = screen.get_height() / 3


def draw_menu():
    ground.draw()
    dino.draw()
    menu_text = font.render("Main Menu", True, BLACK)
    menu_text_2 = font.render("press space, Arrow Up or Down", True, BLACK)
    screen_text = font.render("screen mode", True, BLACK)
    screen.blit(menu_text, (screen.get_width() / 2, screen.get_height() / 10))
    screen.blit(menu_text_2, (screen.get_width() / 2, screen.get_height() / 5))
    screen.blit(screen_text, (screen.get_width() / 20, screen.get_height() / 20))
    button_resize.draw(screen)


def draw_game(keys):
    nepriyatno_text = font.render("Стоп! Мне не приятно!", True, BLACK)
    game_text = font.render("Game", True, BLACK)
    score_text = font.render(f'score: {int(score)}', True, BLACK)
    game_txt_rect = game_text.get_rect()
    if keys[pygame.K_LEFT]:
        screen.blit(nepriyatno_text, (screen.get_width() / 10, screen.get_height() * 0.6))
    screen.blit(score_text, (screen.get_width() * 0.8, screen.get_height() / 10))
    screen.blit(game_text, (screen.get_width() / 2 - game_txt_rect.width // 2, screen.get_height() / 10))
    if on_ground:
        play_walking_anim()
    ground.draw()
    if not dev_version:
        dino.draw()
        cactus.draw()
    else:
        dino.draw_dev()
        cactus.draw_dev()


def play_walking_anim():
    global dino_state
    global dino_step
    global last_update
    global dino
    global anim_speed

    now = pygame.time.get_ticks()
    if now - last_update > anim_speed:
        if dino_seat == 0:
            dino_step = 1 if dino_step == 2 else 2
            dino.set_image(dino_step + dino_state)
        else:
            dino.set_image(12)
        last_update = now


def game(dt, keys):
    global current_state
    global game_time
    global dino_state
    global dino_seat
    global on_ground

    if not (game_time < 1) and (dino_seat == 0):
        ground.run(current_speed * dt)
        update_score()

    if keys[pygame.K_SPACE]:
        on_ground = False

    if not on_ground:
        jump(dt)

    cactus.set_position((cactus.position[0] - anim_speed * dt, cactus.position[1]))
    print(dino.position, cactus.cactus_array[0].bounds[0].topleft)

    dino_seat = 1 if keys[pygame.K_LEFT] else 0
    dino_state = 2 if keys[pygame.K_DOWN] else 0

    if detect_collision():
        print("yeas")
        current_state = GameState.MENU
        spawn_all_entitys()

    update_speed(dt)


def jump(dt):
    global jump_height, dino_start_position_y, on_ground, dino, jump_time, jump_duration

    jump_time += dt

    if jump_duration == 0:
        jump_duration = 1.0

    progress = jump_time / jump_duration

    if progress <= 1.0:
        height_factor = math.sin(math.pi * progress)
        current_height = jump_height * height_factor
        new_y = dino_start_position_y - current_height
        dino.set_position((dino.position[0], new_y))
    else:
        dino.position = (dino.position[0], dino_start_position_y)
        jump_time = 0
        jump_duration = 0
        on_ground = True


def detect_collision():
    global dino
    global cactus

    for i in (range(len(cactus.cactus_array))):
        for p in dino.collide_points:
            if cactus.cactus_array[i].collide_with_point(p):
                return True

    return False


def resize():
    global dino, screen, ground_height, font, button_resize

    if button_resize.text == "MI":
        button_resize.text = "MA"
        screen = pygame.display.set_mode(Resolutions.MIN)
        ground_height = screen.get_height() * 0.85
        font = pygame.font.Font(None, screen.get_height() // 20)

        spawn_all_entitys()

    elif button_resize.text == "MA":
        button_resize.text = "MI"
        screen = pygame.display.set_mode(Resolutions.MAX)
        ground_height = screen.get_height() * 0.85
        font = pygame.font.Font(None, screen.get_height() // 20)
        spawn_all_entitys()


def update_score():
    global game_time, score
    score = game_time * 8.5 + current_speed / 100


def update_speed(dt):
    global current_speed, game_time
    game_time += dt
    if current_speed < max_speed:
        current_speed = min(max_speed, base_speed + acceleration_rate * game_time)


def reset_speed():
    global current_speed, game_time
    current_speed = base_speed
    game_time = 0


def main(args):
    global current_state, dino_state, dino_step, dino_seat, last_time, dev_version

    if len(args) != 1:
        dev_version = True
    else:
        dev_version = False

    spawn_all_entitys()
    running = True
    dino.set_image(1)
    while running:
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        dt = (current_time - last_time) / 1000
        last_time = current_time
        dt = min(dt, 1.0 / FPS_limit * 2)

        mouse_pos = pygame.mouse.get_pos()
        screen.fill(color)

        if current_state == GameState.MENU:
            draw_menu()
            button_resize.is_hovered(mouse_pos)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                elif button_resize.is_clicked(mouse_pos, event):
                    resize()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        current_state = GameState.GAME

        elif current_state == GameState.GAME:

            draw_game(keys)
            game(dt, keys)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        pass

        pygame.display.flip()
        clock.tick(FPS_limit)


if __name__ == '__main__':
    main(sys.argv)
