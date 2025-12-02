import pygame
import os
from constants import *


class Entity:
    def __init__(self, screen: pygame.Surface, folder_name, position=(0.0, 0.0), width=64):
        self.screen = screen

        self.condition_aray = {}
        self.load_images(folder_name)
        self.image_n = 0
        self.ready_image = self.condition_aray[self.image_n]

        self.sch = self.ready_image.get_width() / self.ready_image.get_height()
        self.ready_image = pygame.transform.scale(self.ready_image, (width, width // self.sch))

        self.position = (position[0], position[1] - self.ready_image.get_height())
        self.center = (self.position[0] + self.ready_image.get_width() / 2,
                       self.position[1] + self.ready_image.get_height() / 2)

    def load_images(self, folder_name):
        count = 0
        dir_path = SRC_IMAGES + folder_name
        for path in os.scandir(dir_path):
            if path.is_file():
                count += 1
        print('file count:', count)
        try:
            for i in range(count):
                self.condition_aray[i] = pygame.image.load(
                    f'{SRC_IMAGES}{folder_name}/{folder_name}_{i}.png').convert_alpha()
        except Exception as E:
            print(f'ошибка загрузки спрайтов: {E}')

    def scale_img(self, width):
        self.ready_image = pygame.transform.scale(self.ready_image, (width, width / self.sch))

    def update_center(self):
        self.center = (self.ready_image.get_rect().center[0] + self.position[0],
                       self.ready_image.get_rect().center[1] + self.position[1])

    def draw_dev(self):
        self.update_center()
        self.screen.blit(self.ready_image, self.position)
        pygame.draw.circle(self.screen, BLUE, self.center, 5)
        pygame.draw.circle(self.screen, RED, self.position, 5)

    def draw(self):
        self.screen.blit(self.ready_image, (round(self.position[0]), round(self.position[1])))

    def set_image(self, num):
        try:
            width = self.ready_image.get_width()
            self.ready_image = self.condition_aray[num]
            self.scale_img(width)
        except Exception as E:
            print(f'ошибка использования спрайта: {E}')

    def set_position(self, position):
        self.position = position
        self.update_center()

    def get_h(self):
        return self.ready_image.get_height()

    def get_w(self):
        return self.ready_image.get_width()

    def move_x(self, x_offset):
        self.position = (self.position[0] + x_offset, self.position[1])

    def move_y(self, y_offset):
        self.position = (self.position[0], self.position[1] + y_offset)
