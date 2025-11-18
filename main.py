import pygame


pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("Dino")
clock = pygame.time.Clock()
color = 0

class Entity:
    def __init__(self, path_to_image: str, position = (0, 0) , scale = 1.0):
        try:
            self.image: pygame.surface = pygame.image.load(path_to_image)
        except Exception as E:
            print(f'ошибка открытия изображения: {E}')
        self.image = pygame.transform.scale(self.image , (int(self.image.get_width()*scale) , (self.image.get_height()*scale)))

        self.rect = self.image.get_rect()
        self.rect.center = position

    def set_position(self, position: tuple[int, int]):
        self.rect.center = position

    def draw(self):
        screen.blit(self.image, self.rect.center)


def main():
    dino = Entity('src/images/dino.png', (50, 50), 1)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((color, color, color))

        dino.draw()

        pygame.display.flip()
        clock.tick(60)



if __name__ == '__main__':
    main()
