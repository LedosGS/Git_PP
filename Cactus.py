import pygame
import random
from Entity import *


class Cactus:
    def __init__(self, screen: pygame.Surface, folder_name, position=(0, 0), width=64, min_scale=0.5, max_scale=1):
        self.count = random.randint(1, 3)
        self.position = position
        self.ents = []
        for i in range(self.count):
            image_n = random.randint(0, 2)
            bound_point = EMPTY4
            if image_n == 0:
                bound_point = (width / 13.5, width/2.1)
            self.ents.append(Entity(screen, folder_name, position, width, bound_point))
            self.ents[i].set_image(image_n)
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
