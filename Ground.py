from Entity import *


class Ground:
    def __init__(self, screen: pygame.Surface, folder_name, position=(0, 0), width=64):
        self.ent = Entity(screen, folder_name, position, width)
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