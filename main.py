import pygame
import func
from classes import Button, cwd, MajorCountrySelect, Map, MinorCountrySelect
from json import load, dump

import enum

with open("settings.json") as json_data:
    settings_json = load(json_data)
    scrollinvert = settings_json["Scroll Invert"]

pygame.init()
screen = pygame.display.set_mode(
    (1920, 1080), pygame.DOUBLEBUF | pygame.SCALED, vsync=1
)

# NOTE(pol): What is this variable for?
menu = True

Menu = enum.Enum('Menu', 'main_menu countryselect settings game')
current_menu = Menu.main_menu

# themeing shit
menubg = pygame.image.load(f"{cwd}/ui/menu.png")
tab = [1]
scroll = 0
color = 0

tick = mscroll = 0
player_country = None
mtogg = False

map = Map("Modern World")


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
    Button("Back", (1125, 570), (160, 40), 5),
    Button("Map Select", (1375, 570), (160, 40), 5),
    Button("Country List", (1125, 670), (160, 40), 5),
    Button("Start", (1375, 670), (160, 40), 5),
]

sprites = pygame.sprite.Group()
countrymajor = MajorCountrySelect("starts/Modern World/majors.txt", 5, sprites )
countryminor = MinorCountrySelect("starts/Modern World/minors.txt", 5, sprites)

run = True
while run:
    mpos = pygame.mouse.get_pos()
    print(player_country)
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                run = False

            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_F4:
                        pygame.display.toggle_fullscreen()

            case pygame.MOUSEWHEEL:
                if current_menu == Menu.countryselect:
                    scroll = min(
                        max(scroll - scrollinvert * event.y, 0),
                        len( countrymajor.majors )-5,
                    )
                    # for i in countrymajor.majors:
                    #     i.pos = (i.pos[0], i.pos[1] - scrollinvert * event.y * 200)
                    #     i.brect = pygame.Rect(i.pos[0], i.pos[1], 700, 200)
                    countrymajor.update(scroll)
                else:
                    mscroll = -scrollinvert * event.y
                    if current_menu == Menu.game:
                        map.update(mscroll)
                        # print(map.scale)
                        # map.cvmap =  pygame.transform.scale_by(map.cmap,map.scale)
                mtogg = True

            case pygame.MOUSEBUTTONDOWN:
                mscroll = 0
                mtogg = True
                # if game:
                    # color = screen.get_at(pygame.mouse.get_pos())

            case pygame.MOUSEBUTTONUP | pygame.MOUSEMOTION:
                mscroll = 0
                mtogg = False

    # NOTE(pol): I noticed a bunch of repeating patterns.
    # This is not very nice for drawing UI elements, I might extract stuff
    # into more convenient functions.
    # Also, mixing button press logic and rendering seems evil but whatever.
    if current_menu != Menu.game:
        screen.blit(menubg, (0, 0))

        if current_menu == Menu.main_menu:
            for i in menubuttons:
                if i.draw(screen, mpos, mtogg, settings_json,tick):
                    tab = i.draw(screen, mpos, mtogg, settings_json,tick)

            match tab:
                case "Settings":
                    current_menu = Menu.settings
                case "Start Game":
                    current_menu = Menu.countryselect
                case "Exit":
                    run = False
            tab = 0

        if current_menu == Menu.settings:
            for i in settingsbuttons:
                if i.draw(screen, mpos, mtogg, settings_json,tick):
                    tab = i.draw(screen, mpos, mtogg, settings_json,tick)

            match tab:
                case "Exit":
                    current_menu = Menu.main_menu

                case "UI Size":
                    settings_json["UI Size"] += mscroll
                    settings_json["UI Size"] = func.clamp(settings_json["UI Size"] + mscroll, 14, 40)

                case "Scroll Invert":
                    settings_json["Scroll Invert"] = func.clamp(settings_json["Scroll Invert"], 0, 1)
                    settings_json["Scroll Invert"] = settings_json["Scroll Invert"] * -2 + 1

                case "Sound Volume":
                    settings_json["Sound Volume"] += mscroll
                    settings_json["Sound Volume"] = func.clamp(settings_json["Sound Volume"], 0, 100)

                case "Music Volume":
                    settings_json["Music Volume"] += mscroll
                    settings_json["Music Volume"] = func.clamp(settings_json["Music Volume"], 0, 100)

                case "FPS":
                    settings_json["FPS"] += mscroll
                    settings_json["FPS"] = max(settings_json["FPS"], 12)

            with open("settings.json", "w") as json_data:
                dump(settings_json, json_data)

            mtogg = False
            tab = 0

        if current_menu == Menu.countryselect:
            # pygame.draw.rect(screen, (50, 50, 50), ((300, 40), (1200, 1000)), 0, 20)
            # pygame.draw.rect(screen, (40, 40, 40), ((1000, 540), (500, 200)), 0, 20)
            sprites.draw(screen)
            pygame.draw.rect(countrymajor.image, (40, 40, 40), ((00, 0), (700, 1000)), 0, 20)
            i = 0
            for major in countrymajor.majors[countrymajor.min:countrymajor.max:]:
                major.pos[1] = i 
                i += 200
                if major.draw(countrymajor.image, mpos, player_country, mtogg):
                    player_country = major.draw(
                        countrymajor.image, mpos, player_country, mtogg
                    )
            i = 0

            for minor in countryminor.minors[countryminor.min:countryminor.max:]:
                if minor.draw(countryminor.image, mpos, player_country, mtogg):
                    player_country = minor.draw(
                        countryminor.image, mpos, player_country, mtogg
                    )

            for i in countryselectbuttons:
                if i.draw(screen, mpos, mtogg, settings_json,tick):
                    tab = i.draw(screen, mpos, mtogg, settings_json,tick)

            match tab:
                case "Start":
                    current_menu = Menu.game
                case "Back":
                    current_menu = Menu.main_menu
            tab = 0
    else:
        print( color )
        map.draw(screen)
    
    tick+=1

    pygame.time.Clock().tick(settings_json["FPS"])
    pygame.display.update()
