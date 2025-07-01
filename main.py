import pygame
from CountryData import Countries
import func
from os import getcwd
from classes import (
    Button,
    MajorCountrySelect,
    Map,
    MinorCountrySelect,
    CountryMenu,
    fontalias,
    primary
)
from json import load, dump
from enum import Enum
import globals

Menu = Enum("Menu", "main_menu countryselect settings game")

def main():
    pygame.init()
    screen = pygame.display.set_mode(
        (1920, 1080), pygame.DOUBLEBUF | pygame.SCALED, vsync=1
    )

    settings_json = None
    try:
        with open("settings.json") as json_data:
            settings_json = load(json_data)
    except FileNotFoundError:
        settings_json = {
                "Scroll Invert": -1,
                "UI Size": 14,
                "FPS": 139,
                "Sound Volume": 0,
                "Music Volume": 0,
                }
        with open("settings.json", "w") as json_data:
            dump(settings_json, json_data)

    scrollinvert = settings_json["Scroll Invert"]
    globals.ui_scale = int(settings_json["UI Size"] / 14)

    pygame.font.init()
    cwd = getcwd()
    ui_font = pygame.font.Font(f"{cwd}/ui/font.ttf", 24 * globals.ui_scale)
    title_font = pygame.font.Font(f"{cwd}/ui/font.ttf", 64 * globals.ui_scale)

    menubg = pygame.image.load("ui/menu.png")
    game_title = title_font.render("Souls Of Metal", fontalias, primary)
    game_logo = pygame.image.load("ui/logo.png").convert_alpha()

    current_menu = Menu.main_menu
    tick = 0
    mouse_pressed = False

    sprites = pygame.sprite.Group()
    major_country_select = MajorCountrySelect("starts/Modern World/majors.txt", 5, ui_font, sprites)
    minor_country_select = MinorCountrySelect("starts/Modern World/minors.txt", 5, sprites)
    selectmenu = CountryMenu()
    with open("CountryData.json") as json_data:
        countries_data = load(json_data)
    countries = Countries(countries_data)
    map = Map("Modern World", (0, 0), 1)

    player_country = None

    selected_country_rgb = 0

    menubuttons = [
        Button("Start Game", (200, 400), (160, 40), 5),
        Button("Continue Game", (200, 500), (160, 40), 5),
        Button("Settings", (200, 600), (160, 40), 5),
        Button("Credits", (200, 700), (160, 40), 5),
        Button("Exit", (200, 800), (160, 40), 5)
    ]

    settingsbuttons = [
        Button("UI Size",       (200, 200), (160, 40), 5),
        Button("FPS",           (200, 300), (160, 40), 5),
        Button("Sound Volume",  (200, 400), (160, 40), 5),
        Button("Music Volume",  (200, 500), (160, 40), 5),
        Button("Scroll Invert", (200, 600), (160, 40), 5),
        Button("Save Settings", (200, 800), (160, 40), 5),
        Button("Exit", (200, 900), (160, 40), 5)
    ]

    countryselectbuttons = [
        Button("Back", (1125, 570), (160, 40), 5),
        Button("Map Select", (1375, 570), (160, 40), 5),
        Button("Country List", (1125, 670), (160, 40), 5),
        Button("Start", (1375, 670), (160, 40), 5)
    ]

    global global_run
    global_run = True
    while global_run:
        mouse_rel = pygame.mouse.get_rel()
        mouse_pos = pygame.mouse.get_pos()
        mouse_scroll = 0

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    global_run = False

                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_F4:
                            pygame.display.toggle_fullscreen()

                case pygame.MOUSEWHEEL:
                    # mouse_pressed = True
                    mouse_scroll = -scrollinvert * event.y

                    if current_menu == Menu.countryselect:
                        major_country_select.update(mouse_scroll)
                        major_country_select.scroll -= mouse_scroll
                        major_country_select.scroll = func.clamp(
                            major_country_select.scroll,
                            0,
                            len(major_country_select.majors) - 5
                        )
                        major_country_select.min = major_country_select.scroll
                        major_country_select.max = min(len(major_country_select.majors), 6 + major_country_select.scroll)
                    elif current_menu == Menu.game:
                        map.scale = func.clamp(map.scale - (mouse_scroll / 25), 1, 2)
                        map.cvmap = pygame.transform.scale_by(map.cmap, map.scale)
                        map.pos[0] = -mouse_pos[0] * (map.scale - 1)
                        map.pos[1] = -mouse_pos[1] * (map.scale - 1)

                case pygame.MOUSEBUTTONDOWN:
                    mouse_pressed = True
                    r, g, b, _ = screen.get_at(pygame.mouse.get_pos())
                    selected_country_rgb = (r, g, b)

                case pygame.MOUSEBUTTONUP:
                    mouse_pressed = False

        if current_menu != Menu.game:
            screen.blit(menubg, (0, 0))

            if current_menu == Menu.main_menu:
                screen.blit(game_title, (400, 160))

                # NOTE(soi): dear god someone make the logo position look better
                screen.blit(game_logo, (30, 30))

                for button in menubuttons:
                    hovered = button.draw(screen, mouse_pos, mouse_pressed, settings_json, tick, ui_font)
                    if not mouse_pressed or not hovered:
                        continue

                    match button.id:
                        case "Settings":
                            current_menu = Menu.settings
                        case "Start Game":
                            current_menu = Menu.countryselect
                        case "Exit":
                            global_run = False

            elif current_menu == Menu.settings:
                for button in settingsbuttons:
                    hovered = button.draw(screen, mouse_pos, mouse_pressed, settings_json, tick, ui_font)

                    if not hovered:
                        continue

                    match button.id:
                        case "UI Size":
                            settings_json["UI Size"] += mouse_scroll
                            settings_json["UI Size"] = func.clamp(
                                settings_json["UI Size"] + mouse_scroll, 14, 40
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

                    if not mouse_pressed:
                        continue
                        
                    match button.id:
                        case "Scroll Invert":
                            settings_json["Scroll Invert"] = func.clamp(
                                settings_json["Scroll Invert"], 0, 1
                            )
                            settings_json["Scroll Invert"] = (
                                settings_json["Scroll Invert"] * -2 + 1
                            )

                        case "Save Settings":
                            with open("settings.json", "w") as json_data:
                                dump(settings_json, json_data)

                        case "Exit":
                            current_menu = Menu.main_menu

            elif current_menu == Menu.countryselect:
                # pygame.draw.rect(screen, (50, 50, 50), ((300, 40), (1200, 1000)), 0, 20)
                # pygame.draw.rect(screen, (40, 40, 40), ((1000, 540), (500, 200)), 0, 20)
                sprites.draw(screen)
                pygame.draw.rect(
                    major_country_select.image, (40, 40, 40), ((00, 0), (700, 1000)), 0, 20
                )

                country_height = 0
                for major in major_country_select.majors[major_country_select.min : major_country_select.max :]:
                    major.pos[1] = country_height
                    country_height += 200
                    hovered = major.draw(major_country_select.image, mouse_pos, player_country, mouse_pressed)
                    if not mouse_pressed or not hovered:
                        continue

                    player_country = major.id

                for minor in minor_country_select.minors[minor_country_select.min : minor_country_select.max :]:
                    hovered = minor.draw(minor_country_select.image, mouse_pos, player_country, mouse_pressed)
                    if not mouse_pressed or hovered:
                        continue
                    player_country = minor.id

                for button in countryselectbuttons:
                    hovered = button.draw(screen, mouse_pos, mouse_pressed, settings_json, tick, ui_font)
                    if not mouse_pressed or hovered:
                        continue

                    match button.id:
                        case "Start":
                            current_menu = Menu.game
                        case "Back":
                            current_menu = Menu.main_menu
        else:
            map.draw(screen, mouse_rel)
            # print(selected_country_rgb)
            if selected_country_rgb in countries.colorsToCountries:
                selectmenu.draw(
                    screen,
                    countries,
                    countries.colorsToCountries[selected_country_rgb],
                    title_font
                )

        tick += 1

        pygame.time.Clock().tick(settings_json["FPS"])
        pygame.display.update()

main()
