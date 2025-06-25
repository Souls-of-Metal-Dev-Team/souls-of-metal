import pygame
from classes import Button, cwd
from json import load, dump

with open("settings.json") as json_data:
    settings_json = load(json_data)
    scrollinvert = settings_json["scrollinvert"]

initial_settings_json = settings_json
pygame.init()

run = True
menu = True
settings = False
# themeing shit
menubg = pygame.image.load(f"{cwd}/ui/menu.png")
tab = [1]

tick = mscroll = 0
mtogg = False

menubuttons = [
    Button("Start Game", (200, 400), (160, 40), 5),
    Button("Continue Game", (200, 500), (160, 40), 5),
    Button("Settings", (200, 600), (160, 40), 5),
    Button("Credits", (200, 700), (160, 40), 5),
    Button("Exit", (200, 800), (160, 40), 5),
]

settingsbuttons = [
    Button("UI Size", (200, 400), (160, 40), 5),
    Button("FPS", (200, 500), (160, 40), 5),
    Button("Sound Volume", (200, 600), (160, 40), 5),
    Button("Music Volume", (200, 700), (160, 40), 5),
    Button("Exit", (200, 900), (160, 40), 5),
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
                mscroll = -scrollinvert * event.y
                mtogg = True
            case pygame.MOUSEBUTTONDOWN:
                mscroll = 0
                mtogg = True
            # if menu:
            #     for i in menubuttons:
            #         i.check("up", mpos)
            # if settings:
            #     for i in settingsbuttons:
            #         i.check("up", mpos)
            case pygame.MOUSEBUTTONUP:
                mscroll = 0
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
            if i.draw(screen, mpos, mtogg, tab, settings_json):
                tab = i.draw(screen, mpos, mtogg, tab, settings_json)

        match tab:
            case "Settings":
                settings = True
                menu = False
            case "Exit":
                run = False
        tab = 0
    if settings:
        for i in settingsbuttons:
            if i.draw(screen, mpos, mtogg, tab, settings_json):
                tab = i.draw(screen, mpos, mtogg, tab, settings_json)
        match tab:
            case "Exit":
                settings = False
                menu = True
            case _:
                if tab:
                    settings_json[tab] += mscroll
                    if settings_json != initial_settings_json:
                        initial_settings_json = settings_json
                        with open("settings.json", "w") as json_data:
                            dump(settings_json, json_data)

        mtogg = False
        tab = 0

    pygame.display.update()
