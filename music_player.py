import pygame
import os

pygame.init()

# Создание окна
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont(None, 30)

# Папка с музыкой
music_folder = "music"
songs = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
current_index = 0

# Загрузка первой песни
pygame.mixer.music.load(os.path.join(music_folder, songs[current_index]))

def draw_text(text):
    screen.fill((30, 30, 30))
    line = font.render(text, True, (255, 255, 255))
    screen.blit(line, (20, 80))
    pygame.display.flip()

running = True
while running:
    draw_text(f"Now playing: {songs[current_index]}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Управление клавишами
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Play
                pygame.mixer.music.play()
            elif event.key == pygame.K_s:  # Stop
                pygame.mixer.music.stop()
            elif event.key == pygame.K_RIGHT:  # Next
                current_index = (current_index + 1) % len(songs)
                pygame.mixer.music.load(os.path.join(music_folder, songs[current_index]))
                pygame.mixer.music.play()
            elif event.key == pygame.K_LEFT:  # Previous
                current_index = (current_index - 1) % len(songs)
                pygame.mixer.music.load(os.path.join(music_folder, songs[current_index]))
                pygame.mixer.music.play()

pygame.quit()
