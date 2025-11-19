import pygame
import os, math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
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
    def __init__(self, folder_name, position = (0, 0), width = 64):
        self.condition_aray = {}

        count = 0
        dir_path = SRC_IMAGES+folder_name
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
        self.sch = self.ready_image.get_width()/self.ready_image.get_height()
        self.ready_image = pygame.transform.scale(self.ready_image, (width, width//self.sch))
        self.position = (position[0], position[1] - self.ready_image.get_height())


    def set_image(self, num):
        try:
            width = self.ready_image.get_width()
            self.ready_image = self.condition_aray[num]
            self.scale(width)
        except Exception as E:
            print(f'ошибка использования спрайта: {E}')
    def scale(self, width):
        self.ready_image = pygame.transform.scale(self.ready_image, (width, width/self.sch))

    def draw(self):
        screen.blit(self.ready_image, self.position)

    def set_position(self, position):
        self.position = position

    def get_h(self):
        return self.ready_image.get_height()

    def get_w(self):
        return self.ready_image.get_width()

pygame.init()
screen = pygame.display.set_mode(Resolutions.MAX)
pygame.display.set_caption("Dino")
clock = pygame.time.Clock()
info = pygame.display.Info()
color = WHITE
font = pygame.font.Font(None, 36)

current_state = GameState.MENU
ground_height = screen.get_height()*0.85
k = 0
dino_step = 1
dino_state = 0
dino_seat = 0

dino: Entity
ground: Entity
button_resize = Button(screen.get_width()/20, screen.get_width()/20 , screen.get_width()/20, screen.get_width()/20, "MI")

def spawn_all_entitys():
    global dino
    global ground
    global screen

    print(screen.get_width() , screen.get_height())
    dino = Entity('dino', (0, ground_height), screen.get_height() // 4)
    ground = Entity('road', (0, ground_height), screen.get_height() * 2)

def draw_menu():
    ground.draw()
    dino.draw()
    menu_text = font.render("Main Menu", True, BLACK )
    menu_text_2 = font.render("press space, Arrow Up or Down", True, BLACK)
    screen_text = font.render("screen mode", True, BLACK)
    text_rect = menu_text.get_rect()
    text_rect_2 = menu_text_2.get_rect()
    screen_rect = screen_text.get_rect()
    screen.blit(menu_text, (screen.get_width()/2, screen.get_height()/10))
    screen.blit(menu_text_2, (screen.get_width() / 2, screen.get_height() / 5))
    screen.blit(screen_text, (screen.get_width() / 20, screen.get_height() / 20))
    button_resize.draw(screen)

def draw_game():
    menu_text = font.render("Game", True, BLACK)
    text_rect = menu_text.get_rect()
    screen.blit(menu_text, (screen.get_width() / 2, screen.get_height() / 10))
    ground.draw()
    dino.draw()

def game():
    global k
    draw_game()
    dino.set_position((0, math.sin(k)))
    k += 1
    if k > 6:
        k = 0

def resize():
    global dino
    global screen
    global ground_height
    if button_resize.text == "MI":
        button_resize.text = "MA"
        screen = pygame.display.set_mode(Resolutions.MIN)
        ground_height = screen.get_height() * 0.85
        spawn_all_entitys()

    elif button_resize.text == "MA":
        button_resize.text = "MI"
        screen = pygame.display.set_mode(Resolutions.MAX)
        ground_height = screen.get_height() * 0.85
        spawn_all_entitys()


def draw_point(surface, color, position, size=2):
    """Рисует точку в указанной позиции"""
    pygame.draw.circle(surface, color, position, size)


def main():
    global current_state, dino_state, dino_step, dino_seat

    spawn_all_entitys()
    running = True
    dino.set_image(1)
    while running:
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

                    if event.key == pygame.K_RIGHT:
                        if dino_step == 2:
                            dino_step = 1
                        else:
                            dino_step += 1
                        dino.set_image(dino_step + dino_state)

                    if event.key == pygame.K_LEFT:
                        if dino_seat == 1:
                            dino_seat = 0
                            dino.set_image(0)
                        else:
                            dino_seat = 1
                            dino.set_image(12)

                    if event.key == pygame.K_DOWN:
                        if dino_state == 2:
                            dino_state = 0
                        else:
                            dino_state += 2
                        dino.set_image(dino_step + dino_state)

        elif current_state == GameState.GAME:
            game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        pass


        draw_point(screen, BLUE, dino.position)
        pygame.display.flip()
        clock.tick(60)





if __name__ == '__main__':
    main()
