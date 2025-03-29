import pygame, sys

pygame.init()

# --------------------------------------------------
# НАСТРОЙКИ И КОНСТАНТЫ
# --------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60

# Размер левой панели инструментов
TOOLBAR_WIDTH = 80

# Список цветов для палитры
COLOR_PALETTE = [
    (0, 0, 0),       # Чёрный
    (255, 255, 255), # Белый
    (255, 0, 0),     # Красный
    (0, 255, 0),     # Зелёный
    (0, 0, 255),     # Синий
    (255, 255, 0),   # Жёлтый
    (255, 128, 0),   # Оранжевый
    (128, 0, 128)    # Фиолетовый
]

# Начальные значения
current_color = (0, 0, 0)   # Текущий цвет (по умолчанию чёрный)
tool = "pencil"             # Текущий инструмент: pencil, eraser, rect, circle
brush_size = 5              # Начальный размер кисти
drawing = False             # Флаг рисования (зажата ли кнопка мыши)
start_pos = (0, 0)          # Начальная точка для прямоугольников / окружностей
fill_shapes = False         # Режим заливки фигур (True = заливать, False = только контур)

# Создаём окно и экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint+ (улучшенная версия)")

clock = pygame.time.Clock()

# Создаём «холст» для рисования
canvas = pygame.Surface((WIDTH - TOOLBAR_WIDTH, HEIGHT))
canvas.fill((255, 255, 255))  # изначально белый фон на canvas

# Переменная, чтобы рисовать «плавную линию» карандашом/ластиком
last_mouse_pos = None

# --------------------------------------------------
# ФУНКЦИИ
# --------------------------------------------------
def draw_toolbar():
    """
    Рисуем слева панель инструментов:
    - Кнопки переключения инструментов (Pencil, Eraser, Rect, Circle)
    - Выбор режима заливки (Fill)
    - Палитру цветов
    - Текущий цвет и размер кисти
    """
    # Задний фон панели
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, TOOLBAR_WIDTH, HEIGHT))

    font = pygame.font.SysFont("Arial", 16, bold=True)

    # Кнопки инструментов
    screen.blit(font.render("Pencil", True, (0, 0, 0)), (10, 20))
    screen.blit(font.render("Eraser", True, (0, 0, 0)), (10, 50))
    screen.blit(font.render("Rect",   True, (0, 0, 0)), (10, 80))
    screen.blit(font.render("Circle", True, (0, 0, 0)), (10, 110))

    # Кнопка Fill/Outline
    mode_text = "Fill: ON" if fill_shapes else "Fill: OFF"
    screen.blit(font.render(mode_text, True, (0, 0, 0)), (10, 140))

    # Надпись «Colors»
    screen.blit(font.render("Colors:", True, (0, 0, 0)), (10, 180))

    # Квадратики цветов
    y_offset = 210
    for i, col in enumerate(COLOR_PALETTE):
        rect_y = y_offset + i * 25
        pygame.draw.rect(screen, col, (10, rect_y, 20, 20))

    # Текущий цвет
    screen.blit(font.render("Current:", True, (0, 0, 0)), (10, 420))
    pygame.draw.rect(screen, current_color, (10, 445, 20, 20))

    # Размер кисти
    size_text = font.render(f"Size: {brush_size}", True, (0, 0, 0))
    screen.blit(size_text, (10, 480))

    # Подсказка про «+ / -»
    hint_text = font.render("+/- to change size", True, (0, 0, 0))
    screen.blit(hint_text, (10, 500))

    # Подсказка «Ctrl+S = Save»
    hint_save = font.render("Ctrl+S to Save", True, (0, 0, 0))
    screen.blit(hint_save, (10, 540))


def handle_toolbar_click(mx, my):
    """
    Проверяем, куда пользователь кликнул на панели инструментов.
    Меняем инструмент, цвет, режим заливки и т.д.
    """
    global tool, current_color, fill_shapes

    # Клики по кнопкам инструментов
    if 20 <= my <= 35:
        tool = "pencil"
    elif 50 <= my <= 65:
        tool = "eraser"
    elif 80 <= my <= 95:
        tool = "rect"
    elif 110 <= my <= 125:
        tool = "circle"
    elif 140 <= my <= 155:
        # Переключаем fill_shapes
        fill_shapes = not fill_shapes
    else:
        # Палитра
        # Начинается с y=210, каждая цветовая ячейка по 25px высотой
        if 10 <= mx <= 30 and my >= 210:
            idx = (my - 210) // 25
            if 0 <= idx < len(COLOR_PALETTE):
                current_color = COLOR_PALETTE[idx]


def draw_shape_preview():
    """
    В режиме rect/circle при зажатой мыши показываем «превью» фигуры,
    чтобы пользователь видел, что получится.
    """
    if tool not in ("rect", "circle"):
        return

    # Координаты мыши в canvas
    mouse_x, mouse_y = pygame.mouse.get_pos()
    canvas_mouse_x = mouse_x - TOOLBAR_WIDTH
    canvas_mouse_y = mouse_y

    # Начальные координаты тоже в canvas
    x1, y1 = start_pos
    x2, y2 = canvas_mouse_x, canvas_mouse_y

    preview_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    if tool == "rect":
        # Рассчитываем прямоугольник
        rect_x = min(x1, x2)
        rect_y = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        thickness = 0 if fill_shapes else 2  # 0 = залить
        pygame.draw.rect(preview_surf, (*current_color, 100), (TOOLBAR_WIDTH + rect_x, rect_y, w, h), thickness)
    else:
        # Рассчитываем окружность
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        r = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5 / 2)
        thickness = 0 if fill_shapes else 2
        pygame.draw.circle(preview_surf, (*current_color, 100), (TOOLBAR_WIDTH + cx, cy), r, thickness)

    screen.blit(preview_surf, (0, 0))


def save_canvas(filename="my_drawing.png"):
    """
    Сохраняем текущий canvas в PNG-файл.
    """
    pygame.image.save(canvas, filename)
    print(f"Canvas saved to {filename}")


# --------------------------------------------------
# ОСНОВНАЯ ФУНКЦИЯ
# --------------------------------------------------
def main():
    global drawing, start_pos, last_mouse_pos, tool, brush_size

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Управление размером кисти
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # SHIFT + =
                    brush_size += 1
                elif event.key == pygame.K_MINUS:
                    brush_size = max(1, brush_size - 1)

                # Сохранение при Ctrl+S
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_canvas()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if mx < TOOLBAR_WIDTH:
                    # Клик по панели инструментов
                    handle_toolbar_click(mx, my)
                else:
                    # Начало рисования
                    drawing = True
                    last_mouse_pos = (mx - TOOLBAR_WIDTH, my)
                    start_pos = last_mouse_pos

                    # Если Pencil/Eraser — сразу ставим точку
                    if tool in ("pencil", "eraser"):
                        color = current_color if tool == "pencil" else (255, 255, 255)
                        pygame.draw.circle(canvas, color, last_mouse_pos, brush_size // 2)

            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    drawing = False
                    # Если это прямоугольник или круг — финализируем рисунок
                    if tool in ("rect", "circle"):
                        mx, my = event.pos
                        x2, y2 = mx - TOOLBAR_WIDTH, my
                        x1, y1 = start_pos
                        if tool == "rect":
                            rect_x = min(x1, x2)
                            rect_y = min(y1, y2)
                            w = abs(x2 - x1)
                            h = abs(y2 - y1)
                            thickness = 0 if fill_shapes else 2
                            pygame.draw.rect(canvas, current_color, (rect_x, rect_y, w, h), thickness)
                        else:
                            cx = (x1 + x2) // 2
                            cy = (y1 + y2) // 2
                            r = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5 / 2)
                            thickness = 0 if fill_shapes else 2
                            pygame.draw.circle(canvas, current_color, (cx, cy), r, thickness)
                last_mouse_pos = None

            elif event.type == pygame.MOUSEMOTION and drawing:
                mx, my = event.pos
                if tool in ("pencil", "eraser"):
                    # Рисуем линию между last_mouse_pos и текущей позицией
                    color = current_color if tool == "pencil" else (255, 255, 255)
                    new_pos = (mx - TOOLBAR_WIDTH, my)
                    if last_mouse_pos is not None:
                        pygame.draw.line(canvas, color, last_mouse_pos, new_pos, brush_size)
                    last_mouse_pos = new_pos

        # ОТРИСОВКА
        screen.fill((220, 220, 220))  # Фон окна
        # Панель инструментов слева
        draw_toolbar()
        # Холст
        screen.blit(canvas, (TOOLBAR_WIDTH, 0))
        # Превью (для rect/circle)
        if drawing and tool in ("rect", "circle"):
            draw_shape_preview()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
