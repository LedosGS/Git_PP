import pygame
import random

# ===================== НАСТРОЙКИ =====================
WIDTH, HEIGHT = 1200, 400
FPS = 144  # чем выше — тем плавнее (можно и без лимита)
GROUND_Y = 300  # высота земли
CACTUS_SPEED = 450  # пикселей в секунду (можно увеличивать сколько угодно)

# ===================== ИНИЦИАЛИЗАЦИЯ =====================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Плавные кактусы — как в настоящем Chrome Dino")
clock = pygame.time.Clock()

# ===================== ЗАГРУЗКА КАРТИНОК =====================
# Если есть свои спрайты — просто замени пути
try:
    cactus_images = [
        pygame.image.load("./src/images/cactus/cactus_0.png").convert_alpha(),
        pygame.image.load("./src/images/cactus/cactus_1.png").convert_alpha(),
        pygame.image.load("./src/images/cactus/cactus_2.png").convert_alpha(),
    ]
except:
    # Если нет картинок — создаём заглушки
    cactus_images = []
    for size in [(50, 100), (80, 110), (70, 90)]:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (0, 160, 0), surf.get_rect())
        pygame.draw.rect(surf, (0, 200, 0), surf.get_rect().inflate(-10, -10))
        cactus_images.append(surf)


# ===================== КЛАСС КАКТУСА =====================
class Cactus:
    def __init__(self, x):
        self.image = random.choice(cactus_images)
        self.rect = self.image.get_rect()
        self.rect.bottom = GROUND_Y

        # Позиция — float! Это главное для плавности
        self.x = float(x)
        self.y = float(GROUND_Y - self.rect.height)

    def update(self, dt):
        self.x -= CACTUS_SPEED * dt  # плавное движение

    def draw(self, surface):
        # Округляем ТОЛЬКО при отрисовке!
        surface.blit(self.image, (round(self.x), round(self.y)))

    def is_offscreen(self):
        return self.x + self.rect.width < 0


# ===================== СПИСОК КАКТУСОВ И СПАВН =====================
cacti = []
spawn_timer = 0.0
MIN_GAP = 400  # минимальное расстояние между кактусами (в пикселях)
MAX_GAP = 900  # максимальное


def spawn_cactus():
    x = WIDTH + 50
    if cacti:
        last_x = cacti[-1].x + cacti[-1].rect.width
        gap = random.randint(MIN_GAP, MAX_GAP)
        x = last_x + gap
    cacti.append(Cactus(x))


# Первый кактус
spawn_cactus()

# ===================== ГЛАВНЫЙ ЦИКЛ =====================
running = True
while running:
    # === ВАЖНО: правильный dt ===
    dt = clock.tick(FPS) / 1000.0  # секунды с прошлого кадра

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Увеличиваем скорость — проверяем плавность!
                CACTUS_SPEED += 150
                print(f"Скорость: {CACTUS_SPEED} px/s")

    # === Обновление кактусов ===
    for cactus in cacti[:]:
        cactus.update(dt)
        if cactus.is_offscreen():
            cacti.remove(cactus)

    # === Спавн новых ===
    if cacti:
        next_spawn_x = cacti[-1].x + cacti[-1].rect.width + random.randint(MIN_GAP, MAX_GAP)
    else:
        next_spawn_x = WIDTH + 200

    if cacti[0].x < next_spawn_x - WIDTH:
        spawn_cactus()

    # === Отрисовка ===
    screen.fill((135, 206, 250))  # небо как в оригинале

    # Земля
    pygame.draw.line(screen, (83, 53, 10), (0, GROUND_Y), (WIDTH, GROUND_Y), 8)

    # Кактусы
    for cactus in cacti:
        cactus.draw(screen)

    # Инфо
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Скорость: {CACTUS_SPEED:.0f} px/s   Кактусов: {len(cacti)}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()