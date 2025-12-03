import sys
import time

import pygame
import math
# from constants import *
# from Entity import *
from Dino import *
from Button import *
from Ground import *
from Cactus import *
from Clouds import *

dev_version = False
pygame.init()
screen = pygame.display.set_mode(Resolutions.MAX, pygame.SRCALPHA, pygame.DOUBLEBUF | pygame.HWSURFACE)
start_screen = pygame.display.set_mode((200, 400), pygame.SRCALPHA, pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Dino")
clock = pygame.time.Clock()
info = pygame.display.Info()
color = WHITE
font = pygame.font.Font(None, screen.get_height() // 20)
big_font = pygame.font.Font(None, screen.get_height() // 10)

spawn_cactus_system: SpawnSystem
dino: Dino
ground: Ground
clouds: Cloud

current_state = GameState.START_SCREEN
ground_height = screen.get_height() * 0.85
last_time = pygame.time.get_ticks()

dino_step = 1
dino_state = 0
dino_seat = 0
last_update = pygame.time.get_ticks()
anim_speed = 100
dino_image = pygame.image.load(f'{SRC_IMAGES}dino/dino_0.png')
dino_image_2 = pygame.image.load(f'{SRC_IMAGES}dino/dino_5.png')


jump_height = screen.get_height() / 3
on_ground = True
is_jumping = False
dino_start_position_y = 0
jump_duration = 0
jump_time = 0
jump_force = 1.0
difficult_multiply = 1

FPS_limit = 75
base_speed = screen.get_width() / 4
current_speed = base_speed
max_speed = screen.get_width()
acceleration_rate = screen.get_width() / 20
game_time = 0
score = 0.0
max_score = 0

dino_deth_position = (0, 0)

button_resize = Button(screen, screen.get_height() / 10, screen.get_height() / 10, screen.get_height() / 20,
                       screen.get_height() / 20, "MI", font)

button_to_game = Button(start_screen, start_screen.get_width()/10, start_screen.get_height()*0.25, start_screen.get_width() * 0.8, start_screen.get_height()/10, "to game", big_font)

button_dev = Button(start_screen, start_screen.get_width()/10, start_screen.get_height() * 0.45, start_screen.get_width() * 0.8, start_screen.get_height()/10, "relize", big_font)

button_difficult = Button(start_screen, start_screen.get_width()/10, start_screen.get_height() * 0.65, start_screen.get_width() * 0.8, start_screen.get_height()/10, "easy", big_font)
def spawn_all_entitys():
    global dino
    global dino_start_position_y
    global jump_height
    global ground
    global cactus
    global screen
    global spawn_cactus_system
    global base_speed
    global max_speed
    global acceleration_rate
    global button_resize
    global clouds

    spawn_cactus_system = SpawnSystem(screen, ground_height, (0, 0), screen.get_height() / 3)
    clouds = Cloud(screen, 'cloud',
                   (screen.get_width() / 2, screen.get_height() / 2),
                   screen.get_width() // 10)

    dino = Dino(screen, 'dino',
                (0, ground_height),
                screen.get_width() // 10)

    ground = Ground(screen, 'road',
                    (0, ground_height),
                    screen.get_width())

    dino_start_position_y = dino.position[1]
    jump_height = screen.get_width() / 8
    base_speed = screen.get_width() / 4 * difficult_multiply
    max_speed = screen.get_width() * difficult_multiply
    acceleration_rate = screen.get_width() / 35 * difficult_multiply

def draw_start_menu():
    if difficult_multiply == 1:
        start_screen.blit(dino_image, (start_screen.get_width()/2 - dino_image.get_width()/2, start_screen.get_height()*0.8 ))
    else:
        start_screen.blit(dino_image_2, (start_screen.get_width() / 2 - dino_image.get_width() / 2, start_screen.get_height() * 0.8))

    game_over_text = big_font.render(f'Chrome Dino', True, BLACK)
    start_screen.blit(game_over_text, (start_screen.get_width() / 2 - game_over_text.get_width() / 2, start_screen.get_height() / 10))
    button_to_game.draw(start_screen)
    button_dev.draw(start_screen)
    button_difficult.draw(start_screen)


def draw_menu():
    ground.draw()
    dino.draw()
    menu_text = big_font.render("Main Menu", True, BLACK)
    menu_text_2 = font.render("press space, Arrow Up or Down", True, BLACK)
    screen_text = font.render("screen mode", True, BLACK)
    screen.blit(menu_text, (screen.get_width() / 2, screen.get_height() / 10))
    screen.blit(menu_text_2, (screen.get_width() / 2, screen.get_height() / 5))
    screen.blit(screen_text, (screen.get_height() / 7, screen.get_height() / 14))
    button_resize.draw(screen)


def draw_game_over():
    score_text = font.render(f'HI: {int(max_score)}  score: {int(score)}', True, BLACK)
    game_over_text = big_font.render(f'GAME OVER', True, BLACK)
    screen.blit(game_over_text, (screen.get_width()/2 - game_over_text.get_width()/2, screen.get_height() / 10))
    screen.blit(score_text, (screen.get_width() * 0.8, screen.get_height() / 10))
    dino.set_position(dino_deth_position)
    dino.set_image(5)
    clouds.draw()
    dino.draw()
    spawn_cactus_system.draw(dev_version)
    ground.draw()

def draw_game(keys):
    global max_score
    nepriyatno_text = font.render("Стоп! Я устал!", True, BLACK)
    game_text = big_font.render("GAME", True, BLACK)
    score_text = font.render(f'HI: {int(max_score)}  score: {int(score)}    ', True, BLACK)

    if keys[pygame.K_LEFT]:
        screen.blit(nepriyatno_text, (screen.get_width() / 10, screen.get_height() * 0.6))

    screen.blit(score_text, (screen.get_width()-score_text.get_width(), screen.get_height() / 10))
    screen.blit(game_text, (screen.get_width() / 2 - game_text.get_width() / 2, screen.get_height() / 10))
    if on_ground:
        play_walking_anim()
    ground.draw()

    spawn_cactus_system.draw(dev_version)
    if not dev_version:
        clouds.draw()
        dino.draw()
    else:
        clouds.draw()
        dino.draw_dev()


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


def reset_game():
    global on_ground
    global jump_time
    global jump_duration
    dino.position = (dino.position[0], dino_start_position_y)
    jump_time = 0
    jump_duration = 0
    on_ground = True

    reset_speed()


def game(dt, keys):
    global current_state
    global game_time
    global dino_state
    global dino_seat
    global on_ground
    global dino_deth_position

    if not (game_time < 1) and (dino_seat == 0):
        ground.run(current_speed * dt)
        spawn_cactus_system.run(current_speed * dt)
        update_score()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        on_ground = False

    if not on_ground:
        jump(dt)
        if dino.image_n != 0:
            dino.set_image(0)

    dino_seat = 1 if keys[pygame.K_LEFT] else 0
    dino_state = 2 if keys[pygame.K_DOWN] else 0

    if spawn_cactus_system.detect_collision(dino):
        dino_deth_position = dino.position
        reset_game()
        current_state = GameState.GAME_OVER
        save_result(difficult_multiply)

    clouds.run(current_speed * dt)
    update_speed(dt)


def jump(dt):
    global jump_height
    global dino_start_position_y
    global dino
    global jump_time
    global jump_duration
    global on_ground

    jump_time += dt

    if jump_duration == 0:
        jump_duration = 0.65 / difficult_multiply

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

def to_game():
    global current_state
    global screen
    current_state = GameState.MENU
    screen = pygame.display.set_mode(Resolutions.MAX, pygame.SRCALPHA, pygame.DOUBLEBUF | pygame.HWSURFACE)
    resize()

def change_difficult():
    global difficult_multiply
    global button_difficult
    if button_difficult.text == "easy":
        button_difficult.text = "hard"
        difficult_multiply = 2
    else:
        button_difficult.text = "easy"
        difficult_multiply = 1

def dev_choose():
    global button_dev
    global dev_version
    if button_dev.text == "relize":
        button_dev.text = "dev"
        dev_version = True
    else:
        button_dev.text = "relize"
        dev_version = False

def update_button_resize(text):
    global button_resize
    button_resize = Button(screen, screen.get_height() / 7, screen.get_height() / 7, screen.get_height() / 10,
                           screen.get_height() / 10, text, font)

def resize():
    global dino
    global screen
    global ground_height
    global font
    global button_resize
    global big_font

    if button_resize.text == "MI":
        screen = pygame.display.set_mode(Resolutions.MIN)
        ground_height = screen.get_height() * 0.85
        font = pygame.font.Font(None, screen.get_height() // 15)
        big_font = pygame.font.Font(None, screen.get_height() // 10)
        spawn_all_entitys()
        update_button_resize("MA")

    elif button_resize.text == "MA":
        screen = pygame.display.set_mode(Resolutions.MAX)
        ground_height = screen.get_height() * 0.85
        font = pygame.font.Font(None, screen.get_height() // 15)
        big_font = pygame.font.Font(None, screen.get_height() // 10)
        spawn_all_entitys()
        update_button_resize("MI")


def update_score():
    global game_time, score
    score = game_time * 8.5 + current_speed / 100


def update_speed(dt):
    global current_speed, game_time
    game_time += dt
    if current_speed < max_speed:
        current_speed = min(float(max_speed), (base_speed + acceleration_rate * game_time))


def reset_speed():
    global current_speed, game_time, max_score
    max_score = max(score, max_score)
    current_speed = base_speed
    game_time = 0


def main(args):
    global current_state, dino_state, dino_step, dino_seat, last_time, dev_version
    global score

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

        if current_state == GameState.MENU:
            load_result(difficult_multiply)
            screen.fill(color)
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
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        current_state = GameState.GAME

        elif current_state == GameState.GAME:
            screen.fill(color)

            draw_game(keys)
            game(dt, keys)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

        elif current_state == GameState.GAME_OVER:
            screen.fill(color)
            draw_game_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        score = 0
                        spawn_all_entitys()
                        current_state = GameState.MENU

        elif current_state == GameState.START_SCREEN:
            start_screen.fill(color)
            draw_start_menu()
            button_to_game.is_hovered(mouse_pos)
            button_dev.is_hovered(mouse_pos)
            button_difficult.is_hovered(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif button_dev.is_clicked(mouse_pos, event):
                    dev_choose()
                elif button_to_game.is_clicked(mouse_pos, event):
                    to_game()
                elif button_difficult.is_clicked(mouse_pos, event):
                    change_difficult()

        pygame.display.flip()
        clock.tick(FPS_limit)


def save_result(difficult_multiply):
    global max_score
    if difficult_multiply == 1:
        try:
            with open("./src/result.txt", 'w') as f:
                f.write(str(max_score))
        except Exception as E:
            print(f'ошибка открывания файла: {E}')
    else:
        try:
            with open("./src/result_hard.txt", 'w') as f:
                f.write(str(max_score))
        except Exception as E:
            print(f'ошибка открывания файла: {E}')


def load_result(difficult_multiply):
    global max_score
    if difficult_multiply == 1:
        try:
            with open("./src/result.txt", 'r') as f:
                max_score = float(f.read())
        except Exception as E:
            print(f'ошибка открывания файла: {E}')
    else:
        try:
            with open("./src/result_hard.txt", 'r') as f:
                max_score = float(f.read())
        except Exception as E:
            print(f'ошибка открывания файла: {E}')

if __name__ == '__main__':
    main(sys.argv)
