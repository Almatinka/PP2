
import pygame
import datetime

pygame.init()

W, H = 800, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Clock")
clock = pygame.time.Clock()
FPS = 50

clock_face = pygame.image.load("clock.png")
clock_face = pygame.transform.scale(clock_face, (600, 600))

hands = {
    "minute": pygame.transform.scale(pygame.image.load("rightarm.png"), (600, 900)), 
    "second": pygame.transform.scale(pygame.image.load("leftarm.png"), (50, 500)), 
}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    minute, second = now.minute, now.second

    angles = {
        "minute": -minute * 6,
        "second": -second * 6,
    }

    screen.fill((255, 255, 255))
    screen.blit(clock_face, (100, 100))

    for name, img in hands.items():
        rotated = pygame.transform.rotate(img, angles[name])
        rect = rotated.get_rect(center=(W // 2, H // 2))
        screen.blit(rotated, rect.topleft)
        '''Для каждой стрелки: поворачиваем изображение,
находим новую позицию центра и отображаем на экране.'''

    pygame.draw.circle(screen, (0, 0, 0), (W // 2, H // 2), 10)

    pygame.display.flip()
    clock.tick(FPS)
#Обновляем экран и ждём, чтобы не превысить FPS.

pygame.quit()