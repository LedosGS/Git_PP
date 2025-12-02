import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
SRC_IMAGES = "./src/images/"
EMPTY_4 = (0, 0, 0, 0,)
EMPTY_RECT = pygame.Rect(0, 0, 0, 0)


class GameState:
    MENU = 0
    GAME = 1
    GAME_OVER = 2
    START_SCREEN = 3


class Resolutions:
    MIN = (1000, 250)
    MAX = (1200, 300)