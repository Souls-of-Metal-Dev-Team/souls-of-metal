import pygame
from classes import Button, cwd, MajorCountrySelect
from json import load, dump

with open("settings.json") as json_data:
    settings_json = load(json_data)
    scrollinvert = settings_json["Scroll Invert"]

pygame.init()

run = True
menu = True
settings = False
countryselect = False
# themeing shit
menubg = pygame.image.load(f"{cwd}/ui/menu.png")
tab = [1]

tick = mscroll = 0
player_country = None
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
    Button("Scroll Invert", (200, 800), (160, 40), 5),
    Button("Exit", (200, 900), (160, 40), 5),
]

countryselectbuttons = [
    Button("Back", (925, 570), (160, 40), 5),
    Button("Map Select", (1175, 570), (160, 40), 5),
    Button("Country List", (925, 670), (160, 40), 5),
    Button("Start", (1175, 670), (160, 40), 5),
]

a = pygame.sprite.Group()
countrymajor = MajorCountrySelect("starts/Modern World/majors.txt", a)

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
                # if countryselect and (
                #     ((countrymajor.min < 0) and (event.y < 0))
                #     or ((countrymajor.max > 1000) and (event.y > 0))
                # ):
                for i in countrymajor.majors:
                    i.pos = (i.pos[0], i.pos[1] - scrollinvert * event.y * 200)
                    i.brect = pygame.Rect(i.pos[0], i.pos[1], 700, 200)
                    countrymajor.update()
                mscroll = -scrollinvert * event.y
                mtogg = True
            case pygame.MOUSEBUTTONDOWN:
                mscroll = 0
                mtogg = True
            case pygame.MOUSEBUTTONUP:
                mscroll = 0
                mtogg = False

    if menu:
        for i in menubuttons:
            if i.draw(screen, mpos, mtogg, settings_json,tick):
                tab = i.draw(screen, mpos, mtogg, settings_json,tick)

        match tab:
            case "Settings":
                settings = True
                menu = False
            case "Start Game":
                countryselect = True
                menu = False
            case "Exit":
                run = False
        tab = 0
    if settings:
        for i in settingsbuttons:
            if i.draw(screen, mpos, mtogg, settings_json,tick):
                tab = i.draw(screen, mpos, mtogg, settings_json,tick)
        match tab:
            case "Exit":
                settings = False
                menu = True
            case "UI Size":
                settings_json["UI Size"] = max(
                    min(settings_json["UI Size"] + mscroll, 40), 14
                )
            case "Scroll Invert":
                settings_json["Scroll Invert"] = (
                    max(min(settings_json["Scroll Invert"] + mscroll, 1), 0) * -2 + 1
                )
            case "Sound Volume":
                settings_json["Sound Volume"] = max(
                    min(settings_json["Sound Volume"] + mscroll, 100), 0
                )
            case "Music Volume":
                settings_json["Music Volume"] = max(
                    min(settings_json["Music Volume"] + mscroll, 100), 0
                )
            case "FPS":
                settings_json["FPS"] = max(settings_json["FPS"] + mscroll, 12)
        with open("settings.json", "w") as json_data:
            dump(settings_json, json_data)

        mtogg = False
        tab = 0

    if countryselect:
        pygame.draw.rect(screen, (50, 50, 50), ((100, 40), (1200, 1000)), 0, 20)
        pygame.draw.rect(screen, (40, 40, 40), ((800, 540), (500, 200)), 0, 20)
        a.draw(screen)
        countrymajor.update()
        pygame.draw.rect(countrymajor.image, (40, 40, 40), ((0, 0), (700, 1000)), 0, 20)
        for major in countrymajor.majors:
            if major.draw(countrymajor.image, mpos, player_country, mtogg):
                player_country = major.draw(
                    countrymajor.image, mpos, player_country, mtogg
                )
        for i in countryselectbuttons:
            if i.draw(screen, mpos, mtogg, settings_json,tick):
                tab = i.draw(screen, mpos, mtogg, settings_json,tick)

        match tab:
            case "Back":
                countryselect = False
                menu = True
        tab = 0
        print(player_country)
    tick+=1

    pygame.time.Clock().tick(settings_json["FPS"])
    pygame.display.update()
