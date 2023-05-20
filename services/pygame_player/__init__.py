import pygame
import os


pygame.init()

# os.environ["SDL_VIDEODRIVER"] = "dummy"
# pygame..display.init()
display=pygame.display.set_mode((800,600))

virgule1 = pygame.mixer.Sound('virgule4.wav')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               virgule1.play(fade_ms=2000) 
        elif event.type == pygame.QUIT:
            running = False



