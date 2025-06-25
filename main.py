import pygame
from classes import Button, cwd

pygame.init()

run = True
menu = True

# themeing shit
menubg = pygame.image.load(f"{cwd}/ui/menu.png")

startb = Button("Start Game", (200, 400), (160, 40), 5)
continueb = Button("Continue Game", (200, 500), (160, 40), 5)
settingsb = Button("Settings", (200, 600), (160, 40), 5)
exitb = Button("Exit", (200, 700), (160, 40), 5)

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
            case pygame.MOUSEBUTTONDOWN:
                startb.check("up", mpos)
                continueb.check("up", mpos)
                settingsb.check("up", mpos)
                exitb.check("up", mpos)
            case pygame.MOUSEBUTTONUP:
                startb.check("down", mpos)
                continueb.check("down", mpos)
                settingsb.check("down", mpos)
                exitb.check("down", mpos)
    if menu:
        startb.draw(screen, mpos)
        continueb.draw(screen, mpos)
        settingsb.draw(screen, mpos)
        exitb.draw(screen, mpos)

    pygame.display.update()
