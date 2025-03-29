import pygame, sys, random
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# -----------------------------------------
# Константы
# -----------------------------------------
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# События для таймеров
INC_SPEED = USEREVENT + 1  # Увеличение скорости врага и монет
SPAWN_COIN = USEREVENT + 2 # Появление монет

# -----------------------------------------
# Настройка окна и таймера
# -----------------------------------------
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer with Coins - Финальный код")
clock = pygame.time.Clock()

# -----------------------------------------
# Загрузка и масштабирование ресурсов
# -----------------------------------------
# Если исходные изображения слишком большие или маленькие —
# подгоняем их под размеры (примерно 50×100 для машин и ~32×32 для монеты).

# Фон (растягиваем на весь экран)
background_original = pygame.image.load("AnimatedStreet.png")
background = pygame.transform.scale(background_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Машина игрока
player_original = pygame.image.load("Player.png")
player_img = pygame.transform.scale(player_original, (50, 100))

# Машина врага
enemy_original = pygame.image.load("Enemy.png")
enemy_img = pygame.transform.scale(enemy_original, (50, 100))

# Монета
coin_original = pygame.image.load("coin.png")
coin_img = pygame.transform.scale(coin_original, (32, 32))

# Звук аварии
crash_sound = pygame.mixer.Sound("crash.wav")

# Шрифты
font = pygame.font.SysFont("Arial", 30, bold=True)
game_over_font = pygame.font.SysFont("Arial", 50, bold=True)

# -----------------------------------------
# Игровые переменные
# -----------------------------------------
bgY1 = 0
bgY2 = -SCREEN_HEIGHT
speed = 5        # Начальная скорость врага и монет
score = 0        # Счёт (количество пройденных врагов)
coin_count = 0   # Количество собранных монет

# Каждую секунду увеличивать скорость (врага и монет)
pygame.time.set_timer(INC_SPEED, 1000)

# Каждые 2 секунды (2000 мс) спавнить новую монету
pygame.time.set_timer(SPAWN_COIN, 2000)

# -----------------------------------------
# Классы
# -----------------------------------------
class Player(pygame.sprite.Sprite):
    """
    Класс машины игрока.
    Управляется стрелками влево-вправо, не выезжает за пределы экрана.
    """
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # маска для пиксельных коллизий
        self.rect.center = (SCREEN_WIDTH // 2, 520)

    def update(self):
        """Движение влево-вправо по нажатию клавиш со стрелками."""
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)

class Enemy(pygame.sprite.Sprite):
    """
    Вражеская машина, появляется сверху (в случайной позиции X),
    едет вниз и при выезде за экран возвращается обратно.
    """
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.respawn()

    def respawn(self):
        """
        Задаём врагу случайную позицию по X сверху экрана.
        Защищаемся от ситуации, когда спрайт слишком широкий,
        и не влазит в диапазон.
        """
        min_x = self.rect.width // 2
        max_x = SCREEN_WIDTH - self.rect.width // 2
        if max_x < min_x:
            # Если изображение очень большое, подстраховываемся
            min_x = 0
            max_x = SCREEN_WIDTH
        self.rect.center = (random.randint(min_x, max_x), 0)

    def update(self):
        """Движение вниз. Если вышел за экран — возвращается наверх и +1 к счёту."""
        global score
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()
            score += 1

class Coin(pygame.sprite.Sprite):
    """
    Монета, появляется сверху (в случайной позиции X),
    падает вниз и при выходе за нижнюю границу — исчезает.
    """
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.respawn()

    def respawn(self):
        """
        Аналогично врагу, случайная позиция по X,
        учитывая размеры монетки.
        """
        min_x = self.rect.width // 2
        max_x = SCREEN_WIDTH - self.rect.width // 2
        if max_x < min_x:
            min_x = 0
            max_x = SCREEN_WIDTH
        self.rect.center = (random.randint(min_x, max_x), 0)

    def update(self):
        """Падаем вниз. Если вылетели за границу экрана, удаляемся."""
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# -----------------------------------------
# Группы спрайтов
# -----------------------------------------
all_sprites = pygame.sprite.Group()  # все спрайты
enemies = pygame.sprite.Group()      # группа врагов
coins = pygame.sprite.Group()        # группа монет

# Создаём экземпляры
player = Player()
enemy = Enemy()

# Проверяем, чтобы враг при старте не был в игроке
while enemy.rect.colliderect(player.rect):
    enemy.respawn()

# Добавляем в группы
all_sprites.add(player, enemy)
enemies.add(enemy)

# -----------------------------------------
# Основной игровой цикл
# -----------------------------------------
running = True
while running:
    clock.tick(FPS)

    # Обрабатываем события
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Каждую секунду увеличиваем скорость
        if event.type == INC_SPEED:
            speed += 0.5

        # Каждые 2 секунды создаём новую монету
        if event.type == SPAWN_COIN:
            new_coin = Coin()
            all_sprites.add(new_coin)
            coins.add(new_coin)

    # Обновляем все спрайты
    all_sprites.update()

    # Проверяем столкновение с врагами (масочная коллизия)
    if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask):
        crash_sound.play()
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (80, 250))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # Проверяем столкновение с монетами (масочная коллизия).
    # Если столкновение есть, монету убираем (True) и увеличиваем счётчик.
    collected_coins = pygame.sprite.spritecollide(player, coins, True, pygame.sprite.collide_mask)
    coin_count += len(collected_coins)

    # Прокручиваем фон
    bgY1 += 2
    bgY2 += 2
    if bgY1 >= SCREEN_HEIGHT:
        bgY1 = -SCREEN_HEIGHT
    if bgY2 >= SCREEN_HEIGHT:
        bgY2 = -SCREEN_HEIGHT

    # Рисуем фон (две копии для эффекта прокрутки)
    screen.blit(background, (0, bgY1))
    screen.blit(background, (0, bgY2))

    # Рисуем все спрайты
    all_sprites.draw(screen)

    # Пишем счёт (сколько врагов проехали)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Пишем количество собранных монет
    coin_text = font.render(f"Coins: {coin_count}", True, (255, 255, 255))
    screen.blit(coin_text, (SCREEN_WIDTH - 110, 10))

    pygame.display.update()
