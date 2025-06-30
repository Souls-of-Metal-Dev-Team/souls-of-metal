import pygame
from CountryData import Countries
import func
from classes import (
    Button,
    MajorCountrySelect,
    Map,
    MinorCountrySelect,
    CountryMenu,
    title_font,
    fontalias,
    primary,
)
from json import load, dump
from enum import Enum



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

Menu = Enum("Menu", "main_menu countryselect settings game")

def main():
    pygame.init()
    screen = pygame.display.set_mode(
        (1920, 1080), pygame.DOUBLEBUF | pygame.SCALED, vsync=1
    )

    menubg = pygame.image.load("ui/menu.png")
    game_title = title_font.render("Souls Of Metal", fontalias, primary)
    game_logo = pygame.image.load("ui/logo.png").convert_alpha()

    current_menu = Menu.main_menu
    tab = [1]
    tick = 0
    mouse_pressed = False
    mouse_scroll = 0

    sprites = pygame.sprite.Group()
    countrymajor = MajorCountrySelect("starts/Modern World/majors.txt", 5, sprites)
    countryminor = MinorCountrySelect("starts/Modern World/minors.txt", 5, sprites)
    selectmenu = CountryMenu()
    countries = Countries()
    map = Map("Modern World")

    settings_json = None

    try:
        with open("settings.json") as json_data:
            settings_json = load(json_data)
    except FileNotFoundError:
        settings_json = {"Scroll Invert": -1, "UI Size": 14, "FPS": 139, "Sound Volume": 0, "Music Volume": 0}
        with open("settings.json", "w") as json_data:
            dump(settings_json, json_data)

    scrollinvert = settings_json["Scroll Invert"]

    player_country = None

    selected_country = 0

    global global_run
    global_run = True
    while global_run:
        mpos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    global_run = False

                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_F4:
                            pygame.display.toggle_fullscreen()

                case pygame.MOUSEWHEEL:
                    # NOTE(pol): Why are we enabling mtogg here?
                    mouse_pressed = True

                    mouse_scroll = -scrollinvert * event.y

                    if current_menu == Menu.countryselect:
                        countrymajor.update(mouse_scroll)
                        # NOTE(pol): Delete?
                        # for i in countrymajor.majors:
                        #     i.pos = (i.pos[0], i.pos[1] - scrollinvert * event.y * 200)
                        #     i.brect = pygame.Rect(i.pos[0], i.pos[1], 700, 200)

                    elif current_menu == Menu.game:
                            map.update(mouse_scroll, mpos)
                            # NOTE(pol): Delete?
                            # print(map.scale)
                            # map.cvmap =  pygame.transform.scale_by(map.cmap,map.scale)

                case pygame.MOUSEBUTTONDOWN:
                    mouse_pressed = True
                    mouse_scroll = 0
                    r, g, b = screen.get_at(pygame.mouse.get_pos())
                    selected_country = (r, g, b)

                case pygame.MOUSEBUTTONUP | pygame.MOUSEMOTION:
                    mouse_pressed = False
                    mouse_scroll = 0

        if current_menu != Menu.game:
            screen.blit(menubg, (0, 0))

            if current_menu == Menu.main_menu:
                screen.blit(game_title, (400, 160))

                # NOTE(soi): dear god someone make the logo position look better
                screen.blit(game_logo, (30, 30))

                for i in menubuttons:
                    # NOTE(soi): the fact that draw is called twice isnt very efficient so imma store in ina third temp variable
                    temp = i.draw(screen, mpos, mouse_pressed, settings_json, tick)
                    if temp:
                        tab = temp

                match tab:
                    case "Settings":
                        current_menu = Menu.settings
                    case "Start Game":
                        current_menu = Menu.countryselect
                    case "Exit":
                        global_run = False
                tab = 0

            if current_menu == Menu.settings:
                for i in settingsbuttons:
                    temp = i.draw(screen, mpos, mouse_pressed, settings_json, tick)
                    if temp:
                        tab = temp

                match tab:
                    case "Exit":
                        current_menu = Menu.main_menu

                    case "UI Size":
                        settings_json["UI Size"] += mouse_scroll
                        settings_json["UI Size"] = func.clamp(
                            settings_json["UI Size"] + mouse_scroll, 14, 40
                        )

                    case "Scroll Invert":
                        settings_json["Scroll Invert"] = func.clamp(
                            settings_json["Scroll Invert"], 0, 1
                        )
                        settings_json["Scroll Invert"] = (
                            settings_json["Scroll Invert"] * -2 + 1
                        )

                    case "Sound Volume":
                        settings_json["Sound Volume"] += mouse_scroll
                        settings_json["Sound Volume"] = func.clamp(
                            settings_json["Sound Volume"], 0, 100
                        )

                    case "Music Volume":
                        settings_json["Music Volume"] += mouse_scroll
                        settings_json["Music Volume"] = func.clamp(
                            settings_json["Music Volume"], 0, 100
                        )

                    case "FPS":
                        settings_json["FPS"] += mouse_scroll
                        settings_json["FPS"] = max(settings_json["FPS"], 12)

                with open("settings.json", "w") as json_data:
                    dump(settings_json, json_data)

                mouse_pressed = False
                tab = 0

            if current_menu == Menu.countryselect:
                # pygame.draw.rect(screen, (50, 50, 50), ((300, 40), (1200, 1000)), 0, 20)
                # pygame.draw.rect(screen, (40, 40, 40), ((1000, 540), (500, 200)), 0, 20)
                sprites.draw(screen)
                pygame.draw.rect(
                    countrymajor.image, (40, 40, 40), ((00, 0), (700, 1000)), 0, 20
                )
                i = 0
                for major in countrymajor.majors[countrymajor.min : countrymajor.max :]:
                    major.pos[1] = i
                    i += 200
                    temp = major.draw(countrymajor.image, mpos, player_country, mouse_pressed)
                    if temp:
                        player_country = temp
                i = 0

                for minor in countryminor.minors[countryminor.min : countryminor.max :]:
                    temp = minor.draw(countryminor.image, mpos, player_country, mouse_pressed)
                    if temp:
                        player_country = temp
                for i in countryselectbuttons:
                    temp = i.draw(screen, mpos, mouse_pressed, settings_json, tick)
                    if temp:
                        tab = temp

                match tab:
                    case "Start":
                        current_menu = Menu.game
                    case "Back":
                        current_menu = Menu.main_menu
                tab = 0
        else:
            map.draw(screen, pygame.mouse.get_rel())
            print(selected_country)
            if selected_country in countries.colorsToCountries:
                selectmenu.draw(screen, countries.colorsToCountries[selected_country])

        tick += 1

        pygame.time.Clock().tick(settings_json["FPS"])
        pygame.display.update()

main()
