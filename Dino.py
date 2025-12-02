import os
from Entity import *
from constants import *


class Dino(Entity):

    def __init__(self, screen: pygame.Surface, folder_name, position=(0.0, 0.0), width=64):
        super().__init__(screen, folder_name, position, width)
        self.image_n = 0
        self.collide_points = []

    def set_image(self, num):
        try:
            width = self.ready_image.get_width()
            self.image_n = num
            self.ready_image = self.condition_aray[self.image_n]
            self.scale_img(width)
            self.update_collide_points()

        except Exception as E:
            print(f'ошибка использования спрайта: {E}')

    def update_collide_points(self):
        w = self.ready_image.get_width()
        h = self.ready_image.get_height()

        if self.image_n == 3 or self.image_n == 4:
            self.collide_points = [(self.center[0] + w / 2.3, self.center[1] + h/9 ),
                                   (self.center[0] + w / 4.5, self.center[1])]
        else:
            self.collide_points = [(self.center[0] + w / 3.3, self.center[1] - h/7),
                                   (self.center[0] + w / 10, self.center[1] - h/4),
                                   (self.center[0] + w/20, self.center[1] + h/2.7),
                                   (self.center[0] - w/8, self.center[1] + h/2.7),
                                   (self.center[0] - w/3.5, self.center[1] + h/6)]

    def draw(self):
        self.update_collide_points()
        self.update_center()
        self.screen.blit(self.ready_image, self.position)

    def draw_dev(self):
        self.draw()

        pygame.draw.circle(self.screen, BLUE, self.center, 5)
        pygame.draw.circle(self.screen, BLUE, self.position, 5)

        for p in self.collide_points:
            pygame.draw.circle(self.screen, RED, p, 5)
