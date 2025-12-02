import pygame
import random
from Entity import *


class Cloud:

    def __init__(self, screen: pygame.Surface, folder_name, position=(0, 0), width=64, speed=0):
        self.screen = screen
        self.cloud = Entity(screen, folder_name, position, width)

        self.tile_positions = [self.screen.get_width() / 4, self.screen.get_width()]
        self.flag = 1
        self.position = position

    def run(self, speed_dt):

        for i in range(len(self.tile_positions)):
            if self.tile_positions[i] < -self.cloud.get_w():
                self.tile_positions[i] = self.screen.get_width()
                if self.flag == 1:
                    self.flag = 0
                else:
                    self.flag = 1

            self.tile_positions[i] -= speed_dt/10

    def draw(self):
        for i in self.tile_positions:
            ent = self.cloud
            ent.position = (i, ent.position[1])
            ent.draw()
