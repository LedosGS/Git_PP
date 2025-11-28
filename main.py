import sys
from PIL import Image, ImageOps
import pygame
import os, math
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
SRC_IMAGES = "./src/images/"


class GameState:
    MENU = 0
    GAME = 1
    GAME_OVER = 2


class Resolutions:
    MIN = (1000, 500)
    MAX = (1500, 750)


class Button:
    def __init__(self, x, y, width, height, text, color=GRAY, hover_color=DARK_GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        # Рисуем прямоугольник кнопки
        pygame.draw.rect(surface, self.current_color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Обводка

        # Рендерим текст
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        # Проверяем, находится ли курсор над кнопкой
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            return True
        else:
            self.current_color = self.color
            return False

    def is_clicked(self, pos, event):
        # Проверяем, была ли кнопка нажата
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                return True
        return False


class Entity:
    def __init__(self, folder_name, position=(0, 0), width=64, bound_point=(100, 100)):
        self.condition_aray = {}

        count = 0
        dir_path = SRC_IMAGES + folder_name
        for path in os.scandir(dir_path):
            if path.is_file():
                count += 1
        print('file count:', count)
        try:
            for i in range(count):
                self.condition_aray[i] = pygame.image.load(f'{SRC_IMAGES}{folder_name}/{folder_name}_{i}.png')
        except Exception as E:
            print(f'ошибка загрузки спрайтов: {E}')
        self.ready_image = self.condition_aray[0]
        self.sch = self.ready_image.get_width() / self.ready_image.get_height()
        self.ready_image = pygame.transform.scale(self.ready_image, (width, width // self.sch))
        self.position = (position[0], position[1] - self.ready_image.get_height())

        self.x_bound_offset = 0
        self.y_bound_offset = 0
        self.bound_point = bound_point
        if self.bound_point == (0, 0):
            self.center = self.ready_image.get_rect().center
            self.bound_rect = self.ready_image.get_rect()
        else:
            self.center = (self.position[0] + self.ready_image.get_width() / 2, self.position[1] + self.ready_image.get_height() / 2)
            self.bound_rect = pygame.Rect(self.center[0] - self.bound_point[0],
                                          self.center[1] - self.bound_point[1],
                                          2 * (self.center[0] - self.bound_point[0]),
                                          2 * (self.center[1] - self.bound_point[1]))

    def set_image(self, num):
        try:
            width = self.ready_image.get_width()
            self.ready_image = self.condition_aray[num]
            self.scale(width)
        except Exception as E:
            print(f'ошибка использования спрайта: {E}')

    def scale(self, width):
        self.ready_image = pygame.transform.scale(self.ready_image, (width, width / self.sch))

    def update_bound(self):
        self.center = (self.ready_image.get_rect().center[0] + self.position[0] , self.ready_image.get_rect().center[1] + self.position[1])
        self.bound_rect = pygame.Rect(self.center[0] - self.bound_point[0],
                                      self.center[1] - self.bound_point[1],
                                      2 * self.bound_point[0],
                                      2 * self.bound_point[1])

    def draw_bound(self):
        self.update_bound()
        screen.blit(self.ready_image, self.position)

        s = pygame.Surface((self.bound_rect.width, self.bound_rect.height), pygame.SRCALPHA)
        s.fill((255, 0, 0, 128))
        screen.blit(s, self.bound_rect.topleft)
        # pygame.draw.rect(screen, (255, 0, 0, 60), self.bound_rect)

        draw_point(screen, BLUE, self.center, 5)
        draw_point(screen, RED, self.position, 5)



    def draw(self):
        screen.blit(self.ready_image, self.position)

    def set_position(self, position):
        self.position = position
        self.update_bound()

    def get_h(self):
        return self.ready_image.get_height()

    def get_w(self):
        return self.ready_image.get_width()


class Ground:
    def __init__(self, folder_name, position=(0, 0), width=64):
        self.ent = Entity(folder_name, position, width)
        self.tile_positions = [0, self.ent.get_w()]
        self.flag = 1
        self.position = position

    def draw(self):
        for i in self.tile_positions:
            ent = self.ent
            ent.position = (i, ent.position[1])
            ent.draw()

    def run(self, speed):
        for i in range(len(self.tile_positions)):
            if self.tile_positions[i] < -self.ent.get_w():
                self.tile_positions[i] = self.tile_positions[self.flag] + self.ent.get_w()
                if self.flag == 1:
                    self.flag = 0
                else:
                    self.flag = 1

            self.tile_positions[i] -= speed


class Cactus:
    def __init__(self, folder_name, position=(0, 0), width=64, min_scale=0.5, max_scale=1, bound_point=(0, 0)):
        self.count = random.randint(1, 3)
        self.position = position
        self.ents = []
        for i in range(self.count):
            self.ents.append(Entity(folder_name, position, width, bound_point))
            self.ents[i].set_image(random.randint(0, 2))
            self.ents[i].set_position((self.position[0] + i * 100, self.position[1]))

        print(len(self.ents))

    def set_position(self, position=(0, 0)):
        self.position = position
        for i in range(self.count):
            self.ents[i].set_position((self.position[0] + i * 100, self.position[1]))

    def draw(self):
        for i in range(self.count):
            self.ents[i].draw()

    def draw_bound(self):
        for i in range(self.count):
            self.ents[i].draw_bound()


dev_version = False
pygame.init()
screen = pygame.display.set_mode(Resolutions.MAX, pygame.SRCALPHA, pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Dino")
clock = pygame.time.Clock()
info = pygame.display.Info()
color = WHITE
font = pygame.font.Font(None, screen.get_height() // 20)

cactus_2: Cactus
cactus: Cactus
dino: Entity
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


button_resize = Button(screen.get_width() / 20, screen.get_width() / 20, screen.get_width() / 20,
                       screen.get_width() / 20, "MI")


def spawn_all_entitys():
    global dino
    global dino_start_position_y
    global jump_height
    global ground
    global cactus
    global cactus_2
    global screen

    dino = Entity('dino',
                  (0, ground_height),
                  screen.get_height() // 4,
                  (screen.get_width() / 30, screen.get_height() / 10))

    ground = Ground('road',
                    (0, ground_height),
                    screen.get_height() * 2)
    cactus = Cactus('cactus',
                    (screen.get_width() / 2, screen.get_height() / 2),
                    width=(screen.get_height() // 4),
                    bound_point=(screen.get_width() / 30, screen.get_height() / 10))
    cactus_2 = Cactus('cactus',
                    (screen.get_width() / 4, screen.get_height() / 4),
                    width=(screen.get_height() // 4),
                    bound_point=(screen.get_width() / 30, screen.get_height() / 10))

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
        cactus_2.draw()
    else:
        dino.draw_bound()
        cactus.draw_bound()
        cactus_2.draw_bound()


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
    global game_time
    global dino_state
    global dino_seat
    global on_ground
    global jump_force
    global is_space_pressed
    global space_hold_time
    global is_jumping

    if not (game_time < 1) and (dino_seat == 0):
        ground.run(current_speed * dt)
        update_score()

    if keys[pygame.K_SPACE]:
        on_ground = False

    if not on_ground:
        jump(dt)

    cactus.set_position((cactus.position[0] - anim_speed*dt , cactus.position[1]))

    dino_seat = 1 if keys[pygame.K_LEFT] else 0
    dino_state = 2 if keys[pygame.K_DOWN] else 0

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

def detect_collision(dino, cactus):
    pass # пересечение через маски

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


def draw_point(surface, color, position, size=2):
    """Рисует точку в указанной позиции"""
    pygame.draw.circle(surface, color, position, size)


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
