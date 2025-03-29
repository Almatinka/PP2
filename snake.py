import pygame, sys, random

# Инициализация Pygame
pygame.init()

# ----------------------------------------
# НАСТРОЙКИ И КОНСТАНТЫ
# ----------------------------------------
WIDTH, HEIGHT = 600, 600     # Размер игрового окна
BLOCK_SIZE = 20              # Размер одной «клетки», из которой состоит змейка
INITIAL_SPEED = 10           # Начальная скорость (количество «тиков» в секунду)
FOOD_PER_LEVEL = 3           # Количество съеденной еды для перехода на следующий уровень

# Цвета в формате RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED   = (200, 0, 0)
GRAY  = (100, 100, 100)

# Создаём окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Levels")

# Шрифт для вывода текста
font = pygame.font.SysFont("Arial", 24, bold=True)

# ----------------------------------------
# ФУНКЦИИ
# ----------------------------------------
def draw_snake(snake_body):
    """
    Рисует змею на экране.
    Параметр snake_body: список кортежей (x, y) для каждого блока тела змеи.
    """
    for (x, y) in snake_body:
        pygame.draw.rect(screen, GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE))

def get_random_food_pos(snake_body):
    """
    Возвращает (x, y) для еды в случайной позиции.
    Координаты кратны BLOCK_SIZE и не совпадают с координатами змеи.
    Так как у нас нет других «стен» внутри поля, кроме границы,
    главное — не ставить еду на змею.
    """
    while True:
        # Случайные координаты, кратные BLOCK_SIZE
        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        # Проверяем, не заняты ли они змеёй
        if (x, y) not in snake_body:
            return x, y

def check_wall_collision(x, y):
    """
    Проверяем, выходит ли змея за границы окна.
    Если координата < 0 или >= (ширина/высота), то столкновение с «стеной».
    """
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True
    return False

def show_info(score, level):
    """
    Отображение текущего счёта (score) и уровня (level) в верхней части экрана.
    """
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    # Рисуем на экране
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 120, 10))

# ----------------------------------------
# ОСНОВНАЯ ФУНКЦИЯ (игровой цикл)
# ----------------------------------------
def main():
    # Начальные настройки змеи
    # Пусть змея начинается с длиной 3 блока в центре экрана
    start_x = WIDTH // 2
    start_y = HEIGHT // 2
    snake_body = [
        (start_x, start_y),
        (start_x - BLOCK_SIZE, start_y),
        (start_x - 2 * BLOCK_SIZE, start_y)
    ]
    # Направление движения змеи: 'RIGHT', 'LEFT', 'UP', 'DOWN'
    direction = 'RIGHT'

    # Позиция еды
    food_x, food_y = get_random_food_pos(snake_body)

    # Игра продолжается, пока running == True
    running = True
    clock = pygame.time.Clock()

    # Счёт и уровень
    score = 0
    level = 1
    # Текущая скорость (FPS) — растёт при повышении уровня
    speed = INITIAL_SPEED

    # Счётчик, сколько еды съедено на текущем уровне
    food_eaten_this_level = 0

    while running:
        clock.tick(speed)  # ограничиваем FPS в зависимости от текущей скорости

        # ОБРАБОТКА СОБЫТИЙ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Изменяем направление с учётом того, что змейка не может
                # развернуться на 180 градусов за один кадр
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'

        # ЛОГИКА ДВИЖЕНИЯ ЗМЕИ
        # Берём «голову» змейки (первый элемент)
        head_x, head_y = snake_body[0]

        if direction == 'LEFT':
            head_x -= BLOCK_SIZE
        elif direction == 'RIGHT':
            head_x += BLOCK_SIZE
        elif direction == 'UP':
            head_y -= BLOCK_SIZE
        elif direction == 'DOWN':
            head_y += BLOCK_SIZE

        # Проверяем столкновение со стеной (границей окна)
        if check_wall_collision(head_x, head_y):
            running = False

        # Создаём новую голову и добавляем в начало списка
        new_head = (head_x, head_y)
        snake_body.insert(0, new_head)

        # Проверяем, не столкнулись ли мы сами с собой
        # Если «голова» оказывается в том же месте, что и один из блоков тела (кроме головы),
        # значит, змея врезалась в себя
        if new_head in snake_body[1:]:
            running = False

        # Если «голова» съела еду
        if head_x == food_x and head_y == food_y:
            score += 1
            food_eaten_this_level += 1
            # Генерируем новую еду
            food_x, food_y = get_random_food_pos(snake_body)
            # Проверяем, не пора ли повысить уровень
            if food_eaten_this_level >= FOOD_PER_LEVEL:
                level += 1
                food_eaten_this_level = 0
                speed += 2  # Увеличиваем скорость, чтобы сложность росла
        else:
            # Если ничего не съедено, «хвост» удаляем, чтобы длина не росла
            snake_body.pop()

        # ОТРИСОВКА
        screen.fill(BLACK)

        # Рисуем еду (красный квадрат)
        pygame.draw.rect(screen, RED, (food_x, food_y, BLOCK_SIZE, BLOCK_SIZE))

        # Рисуем змею
        draw_snake(snake_body)

        # Отображаем счёт и уровень
        show_info(score, level)

        pygame.display.flip()

    # Если цикл завершён (running = False),
    # значит, произошла «смерть» змейки.
    game_over()

def game_over():
    """
    Функция, которая показывает сообщение «Game Over» и ждёт,
    пока пользователь не закроет окно.
    """
    game_over_font = pygame.font.SysFont("Arial", 50, bold=True)
    go_text = game_over_font.render("GAME OVER", True, WHITE)
    rect = go_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    while True:
        screen.fill(BLACK)
        screen.blit(go_text, rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Запускаем игру
if __name__ == "__main__":
    main()
