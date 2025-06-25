import pygame
from classes import Button, cwd
from json import load

with open("translation.json") as json_data:
    trans = load(json_data)

pygame.init()

run = True
menu = True
settings = False
# themeing shit
menubg = pygame.image.load(f"{cwd}/ui/menu.png")

uisize = 14
fps = 60
sv, mv = 100, 100

menubuttons = [
    Button(trans["Start Game"], (200, 400), (160, 40), 5),
    Button(trans["Continue Game"], (200, 500), (160, 40), 5),
    Button(trans["Settings"], (200, 600), (160, 40), 5),
    Button(trans["Credits"], (200, 700), (160, 40), 5),
    Button(trans["Exit"], (200, 800), (160, 40), 5),
]

settingsbuttons = [
    Button(f"{trans['UI Size']}: {uisize}", (200, 400), (160, 40), 5),
    Button(f"{trans['FPS']}: {fps}", (200, 500), (160, 40), 5),
    Button(f"{trans['Sound Volume']}: {sv}", (200, 600), (160, 40), 5),
    Button(f"{trans['Music Volume']}: {mv}", (200, 700), (160, 40), 5),
    Button(trans["Apply"], (200, 800), (160, 40), 5),
    Button(trans["Exit"], (200, 900), (160, 40), 5),
]

screen = pygame.display.set_mode(
    (1920, 1080), pygame.DOUBLEBUF | pygame.SCALED, vsync=1
)
while run:
    screen.blit(menubg, (0, 0))
    mpos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                run = False
            case pygame.KEYUP:
                match event.key:
                    case pygame.K_F4:
                        pygame.display.toggle_fullscreen()
            case pygame.MOUSEBUTTONDOWN:
                if menu:
                    for i in menubuttons:
                        i.check("up", mpos)
                if settings:
                    for i in settingsbuttons:
                        i.check("up", mpos)
            case pygame.MOUSEBUTTONUP:
                if menu:
                    for i in menubuttons:
                        match i.check("down", mpos):
                            case "Settings":
                                settings = True
                                menu = False
                                break
                            case "Exit":
                                run = False
                if settings:
                    for i in settingsbuttons:
                        match i.check("down", mpos):
                            case "Exit":
                                settings = False
                                menu = True
                                break

    if menu:
        for i in menubuttons:
            i.draw(screen, mpos)
    if settings:
        for i in settingsbuttons:
            i.draw(screen, mpos)

    pygame.display.update()
