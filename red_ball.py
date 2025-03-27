import pygame

pygame.init()

W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Red Ball Control")
clock = pygame.time.Clock()

ball_radius = 25
ball_x = W // 2
ball_y = H // 2
step = 20

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and ball_x - step - ball_radius >= 0:
        ball_x -= step
    if keys[pygame.K_RIGHT] and ball_x + step + ball_radius <= W:
        ball_x += step
    if keys[pygame.K_UP] and ball_y - step - ball_radius >= 0:
        ball_y -= step
    if keys[pygame.K_DOWN] and ball_y + step + ball_radius <= H:
        ball_y += step

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (ball_x, ball_y), ball_radius)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
