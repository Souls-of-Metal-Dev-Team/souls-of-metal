import pygame
from classes import Button, cwd

pygame.init()

run = True
menu = True

# themeing shit
menubg = pygame.image.load(f"{cwd}/ui/menu.png")

startb = Button("Start Game", (100, 100), (120, 40), 5)
screen = pygame.display.set_mode(
    (1920, 1080), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.SCALED, vsync=1
)
while run:
    screen.blit(menubg, (0, 0))
    mpos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                run = False
    if menu:
        startb.draw(screen, mpos)

    pygame.display.update()
