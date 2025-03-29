import pygame, sys

pygame.init()

# --------------------------------------------------
# НАСТРОЙКИ И КОНСТАНТЫ
# --------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60

# Список заранее заданных цветов (для выбора)
COLOR_PALETTE = [
    (0, 0, 0),       # Чёрный
    (255, 255, 255), # Белый
    (255, 0, 0),     # Красный
    (0, 255, 0),     # Зелёный
    (0, 0, 255),     # Синий
    (255, 255, 0)    # Жёлтый
]

# Зададим размеры панели инструментов (слева)
TOOLBAR_WIDTH = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint-like App (Расширенный)")

clock = pygame.time.Clock()

# --------------------------------------------------
# ПОВЕРХНОСТЬ ДЛЯ РИСОВАНИЯ
# --------------------------------------------------
# Будем рисовать не на screen напрямую, а на специальную поверхность (canvas).
# Потом её отображать на экране.
canvas = pygame.Surface((WIDTH - TOOLBAR_WIDTH, HEIGHT))
canvas.fill((255, 255, 255))  # Заливка фона белым

# --------------------------------------------------
# ГЛАВНЫЕ ПЕРЕМЕННЫЕ
# --------------------------------------------------
current_color = (0, 0, 0)  # Текущий цвет (по умолчанию чёрный)
tool = "pencil"            # Инструмент: "pencil", "eraser", "rect", "circle"
brush_size = 5             # Толщина для карандаша/ластика
drawing = False            # Флаг: сейчас рисуем или нет (зажата ли мышь)
start_pos = (0, 0)         # Начальная точка (для рисования прямоугольников, кругов)

# --------------------------------------------------
# ФУНКЦИИ
# --------------------------------------------------
def draw_toolbar():
    """
    Рисует панель инструментов слева: кнопки выбора инструмента,
    цветовую палитру, отображение выбранного цвета.
    """
    # Заливка фона панели серым цветом
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, TOOLBAR_WIDTH, HEIGHT))
    
    # Кнопки инструментов (простые текстовые):
    font = pygame.font.SysFont("Arial", 16, bold=True)
    
    # 1) Pencil
    pencil_text = font.render("Pencil", True, (0, 0, 0))
    screen.blit(pencil_text, (10, 20))
    
    # 2) Eraser
    eraser_text = font.render("Eraser", True, (0, 0, 0))
    screen.blit(eraser_text, (10, 50))
    
    # 3) Rect
    rect_text = font.render("Rect", True, (0, 0, 0))
    screen.blit(rect_text, (10, 80))
    
    # 4) Circle
    circle_text = font.render("Circle", True, (0, 0, 0))
    screen.blit(circle_text, (10, 110))
    
    # Подпишем «Colors»:
    color_title = font.render("Colors:", True, (0, 0, 0))
    screen.blit(color_title, (10, 150))
    
    # Прямоугольнички для цветов
    # Каждый цвет рисуем квадратиком 20×20, с отступом
    y_offset = 180
    for idx, col in enumerate(COLOR_PALETTE):
        rect_x = 10
        rect_y = y_offset + idx * 30
        pygame.draw.rect(screen, col, (rect_x, rect_y, 20, 20))
        
    # Отображение текущего цвета
    current_color_rect_y = y_offset + len(COLOR_PALETTE) * 30 + 20
    screen.blit(font.render("Current:", True, (0, 0, 0)), (10, current_color_rect_y))
    pygame.draw.rect(screen, current_color, (10, current_color_rect_y + 20, 20, 20))

def handle_toolbar_click(pos):
    """
    Обрабатывает щелчок мыши в области панели инструментов.
    Смена инструмента, выбор цвета.
    """
    global tool, current_color
    
    x, y = pos
    # Если клик в зону инструментов (y от 20 до 130 с шагом 30 примерно):
    # Pencil:   y in [20..35]
    # Eraser:   y in [50..65]
    # Rect:     y in [80..95]
    # Circle:   y in [110..125]
    
    if 20 <= y <= 35:
        tool = "pencil"
    elif 50 <= y <= 65:
        tool = "eraser"
    elif 80 <= y <= 95:
        tool = "rect"
    elif 110 <= y <= 125:
        tool = "circle"
    
    # Если клик в зону палитры
    # Палитра начинается с y=180, шаг 30 на каждый цвет
    # Прямоугольники: (10, 180 + i*30, 20, 20)
    if 10 <= x <= 30 and y >= 180:
        idx = (y - 180) // 30  # индекс цвета
        if 0 <= idx < len(COLOR_PALETTE):
            current_color = COLOR_PALETTE[idx]

def draw_shape_preview():
    """
    Если сейчас пользователь «тянет» прямоугольник/круг,
    то отобразим предварительные очертания на экране поверх canvas.
    """
    if tool not in ("rect", "circle"):
        return
    
    # Рисуем на screen поверх canvas
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Переводим в координаты canvas (учитывая смещение панели)
    canvas_mouse_x = mouse_x - TOOLBAR_WIDTH
    canvas_mouse_y = mouse_y
    
    start_x, start_y = start_pos
    # Координаты начала относительно canvas
    x1, y1 = start_x, start_y
    x2, y2 = canvas_mouse_x, canvas_mouse_y
    
    if tool == "rect":
        # Левая верхняя точка и размеры
        rect_x = min(x1, x2)
        rect_y = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        # Прозрачная поверхностная «маска»
        preview_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(preview_surf, (*current_color, 100), (TOOLBAR_WIDTH + rect_x, rect_y, w, h), 2)
        screen.blit(preview_surf, (0, 0))
    else:  # circle
        # Найдём центр и радиус
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        r = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5 / 2)  # расстояние между точками / 2
        preview_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(preview_surf, (*current_color, 100), (TOOLBAR_WIDTH + cx, cy), r, 2)
        screen.blit(preview_surf, (0, 0))

# --------------------------------------------------
# ОСНОВНОЙ ЦИКЛ
# --------------------------------------------------
def main():
    global drawing, start_pos
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Проверяем, не кликнули ли мы в панель инструментов
                if mx < TOOLBAR_WIDTH:
                    handle_toolbar_click((mx, my))
                else:
                    # Начало рисования
                    drawing = True
                    # Запоминаем стартовую точку
                    start_pos = (mx - TOOLBAR_WIDTH, my)
                    
                    if tool == "pencil" or tool == "eraser":
                        # Сразу «ставим точку»
                        color = current_color if tool == "pencil" else (255, 255, 255)
                        pygame.draw.circle(canvas, color, start_pos, brush_size // 2)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    # Завершаем рисование
                    drawing = False
                    
                    # Если рисовали прямоугольник или круг
                    if tool == "rect" or tool == "circle":
                        # Получаем конечную позицию
                        mx, my = event.pos
                        x2, y2 = mx - TOOLBAR_WIDTH, my
                        x1, y1 = start_pos
                        
                        if tool == "rect":
                            # Рисуем прямоугольник на canvas
                            rect_x = min(x1, x2)
                            rect_y = min(y1, y2)
                            w = abs(x2 - x1)
                            h = abs(y2 - y1)
                            pygame.draw.rect(canvas, current_color, (rect_x, rect_y, w, h), 2)
                        else:
                            # Круг
                            cx = (x1 + x2) // 2
                            cy = (y1 + y2) // 2
                            r = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5 / 2)
                            pygame.draw.circle(canvas, current_color, (cx, cy), r, 2)
            
            elif event.type == pygame.MOUSEMOTION and drawing:
                mx, my = event.pos
                
                # Если мы рисуем «карандашом» или «ластиком», то линия идёт следом за мышкой
                if tool == "pencil" or tool == "eraser":
                    color = current_color if tool == "pencil" else (255, 255, 255)
                    
                    # Координаты на canvas
                    canvas_mx = mx - TOOLBAR_WIDTH
                    canvas_my = my
                    
                    # Проводим линию от предыдущей точки к новой
                    # (можно хранить ещё старую координату, но для простоты
                    #  нарисуем маленькую окружность в новой точке)
                    pygame.draw.circle(canvas, color, (canvas_mx, canvas_my), brush_size // 2)
        
        # ОТРИСОВКА НА ЭКРАН
        screen.fill((100, 100, 100))  # общий фон
        
        # Рисуем панель инструментов
        draw_toolbar()
        
        # Рисуем canvas
        screen.blit(canvas, (TOOLBAR_WIDTH, 0))
        
        # Если «тянем» прямоугольник или круг — показываем превью
        if drawing and (tool == "rect" or tool == "circle"):
            draw_shape_preview()
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
