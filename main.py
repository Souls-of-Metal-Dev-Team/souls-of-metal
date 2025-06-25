import pygame
from classes import Button, cwd
from json import load

with open("translation.json") as json_data:
    trans = load(json_data)

with open("settings.json") as json_data:
    settings_json = load(json_data)
    scrollinvert = settings_json["scrollinvert"]

pygame.init()

run = True
menu = True
settings = False
# themeing shit
menubg = pygame.image.load(f"{cwd}/ui/menu.png")
menutab = [1]

tick = mscroll = 0
mtogg = False

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
            case pygame.MOUSEWHEEL:
                mscroll = mscroll - scrollinvert * event.y
            case pygame.MOUSEBUTTONDOWN:
                mtogg = True
            # if menu:
            #     for i in menubuttons:
            #         i.check("up", mpos)
            # if settings:
            #     for i in settingsbuttons:
            #         i.check("up", mpos)
            case pygame.MOUSEBUTTONUP:
                mtogg = False
                # if menu:
                #     for i in menubuttons:
                #
                # if settings:
                #     for i in settingsbuttons:
                #         match i.check("down", mpos):
                #             case "Exit":
                #                 settings = False
                #                 menu = True
                #                 break
    # print(mscroll)

    if menu:
        for i in menubuttons:
            if i.draw(screen, mpos, mtogg, menutab):
                menutab = i.draw(screen, mpos, mtogg, menutab)
            match menutab:
                case "Settings":
                    settings = True
                    menu = False
                    break
                case "Exit":
                    run = False
    if settings:
        for i in settingsbuttons:
            if i.draw(screen, mpos, mtogg, menutab):
                menutab = i.draw(screen, mpos, mtogg, menutab)
            match menutab:
                # case "Sound Volume":
                case "Exit":
                    settings = False
                    menu = True
                    break

    pygame.display.update()
