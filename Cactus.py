import pygame
import random
from Entity import *


class Cactus(Entity):
    def __init__(self, screen: pygame.Surface, folder_name, position=(0, 0), width=64):
        super().__init__(screen, folder_name, position, width)
        self.image_n = random.randint(0, 2)
        # self.image_n = 0
        self.set_image(self.image_n)
        self.bounds = [EMPTY_RECT] * 2
        if self.image_n > 0:
            self.bounds = [EMPTY_RECT] * 3

        self.update_bounds()

    def update_bounds(self):
        self.bounds[0] = pygame.Rect(self.center[0] - self.ready_image.get_width() / 17,
                                     self.center[1] - self.ready_image.get_height() / 2.2,
                                     self.ready_image.get_width() / 7.5,
                                     self.ready_image.get_height() / 1.1)

        self.bounds[1] = pygame.Rect(self.center[0] + self.ready_image.get_width() / 8,
                                     self.center[1] - self.ready_image.get_height() / 3.3,
                                     self.ready_image.get_width() / 10,
                                     self.ready_image.get_height() / 3)

        if self.image_n == 1:
            self.bounds[2] = (pygame.Rect(self.center[0] - self.ready_image.get_width() / 5,
                                          self.center[1] - self.ready_image.get_height() / 6,
                                          self.ready_image.get_width() / 10,
                                          self.ready_image.get_height() / 3))
        elif self.image_n == 2:
            self.bounds[2] = (pygame.Rect(self.center[0] - self.ready_image.get_width() / 4.5,
                                          self.center[1] - self.ready_image.get_height() / 2.8,
                                          self.ready_image.get_width() / 10,
                                          self.ready_image.get_height() / 3))

    def collide_with_point(self, point):
        for rec in self.bounds:
            if rec.collidepoint(point):
                return True
        return False

    def draw(self):
        self.update_bounds()
        self.screen.blit(self.ready_image, self.position)

    def draw_dev(self):
        self.draw()

        for rec in self.bounds:
            s = pygame.Surface((rec.width, rec.height), pygame.SRCALPHA)
            s.fill((255, 0, 0, 128))
            self.screen.blit(s, rec.topleft)

    def scale(self):
        pass


class Cactus_group:
    def __init__(self, screen: pygame.Surface, folder_name, position=(0, 0), width=64, min_scale=0.5, max_scale=1):
        self.count = random.randint(1, 3)
        self.position = position
        self.cactus_array = []
        for i in range(self.count):
            self.cactus_array.append(Cactus(screen, folder_name, position, width))
            self.cactus_array[i].set_position((self.position[0] + i * 100, self.position[1] - self.cactus_array[i].ready_image.get_height()))

    def set_position(self, position=(0, 0)):
        self.position = position
        for i in range(self.count):
            self.cactus_array[i].set_position((self.position[0] + i * 100, self.position[1] - self.cactus_array[i].ready_image.get_height()))

    def draw(self):
        for i in range(self.count):
            self.cactus_array[i].draw()

    def draw_dev(self):
        for i in range(self.count):
            self.cactus_array[i].draw_dev()


class SpawnSystem:
    def __init__(self, screen: pygame.Surface, ground_height):
        self.screen = screen
        self.ground_height = ground_height
        self.groups = []
        self.spawn_cactus()

    def run(self, current_speed, dt):
        for i in range(len(self.groups)):
            if not (self.groups[i].position[0] < -self.screen.get_width()/4):
                self.groups[i].set_position((self.groups[i].position[0] - current_speed * dt, self.groups[i].position[1]))
            else:
                del self.groups[i]
                print(self.groups)
                self.spawn_cactus()


    def spawn_cactus(self):
        self.groups.append(Cactus_group(self.screen, 'cactus',
                    (self.screen.get_width() / 2, self.ground_height),
                    width=(self.screen.get_width() // 10)))

    def show_cactuses(self, dev_version):
        if dev_version:
            for cactus in self.groups:
                cactus.draw_dev()
        else:
            for cactus in self.groups:
                cactus.draw()

    def detect_collision(self, dino):
        for group in self.groups:
            for i in (range(len(group.cactus_array))):
                for p in dino.collide_points:
                    if group.cactus_array[i].collide_with_point(p):
                        return True
        return False