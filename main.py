import pygame
from CountryData import Countries
import func
from os import getcwd
from classes import (
    Button,
    MajorCountrySelect,
    Map,
    MinorCountrySelect,
    fontalias,
    primary,
    secondary,
    tertiary,
)
from json import load, dump
from enum import Enum
import globals
import os
import sys
import datetime


base_path = os.path.dirname(__file__)
if getattr(sys, "frozen", False):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

Menu = Enum("Menu", "MAIN_MENU COUNTRY_SELECT SETTINGS CREDITS GAME ESCAPEMENU")


def main():
    speed = 4
    file_path = os.path.join(base_path, "date.txt")

    with open(file_path) as f:
        lines = f.readlines()
        ymd = lines[0].strip().split(",")
        year = int(ymd[0])
        month = int(ymd[1])
        day = int(ymd[2])
        date = datetime.date(year, month, day)

    display_date = date.strftime("%A, %B %e, %Y")
    pygame.init()
    screen = pygame.display.set_mode(
        (1920, 1080), pygame.DOUBLEBUF | pygame.SCALED, vsync=1
    )

    pygame.mixer.init()

    # Load music
    music_path = os.path.join(base_path, "sound", "music", "background.mp3")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    else:
        print("[WARNING] Music file not found at:", music_path)

    with open(os.path.join(base_path, "translation.json")) as f:
        globals.language_translations = load(f)

    current_menu = Menu.MAIN_MENU
    tick = 0
    mouse_pressed = False
    mouse_scroll = 0

    with open(os.path.join(base_path, "CountryData.json")) as f:
        countries_data = load(f)
    countries = Countries(countries_data)

    settings_json = None
    try:
        with open(os.path.join(base_path, "settings.json")) as f:
            settings_json = load(f)
    except FileNotFoundError:
        settings_json = {
            "Scroll Invert": 1,
            "UI Size": 14,
            "FPS": 144,
            "Sound Volume": 100,
            "Music Volume": 100,
        }
        with open(os.path.join(base_path, "settings.json"), "w") as f:
            dump(settings_json, f)

    globals.ui_scale = settings_json["UI Size"] // 14

    pygame.font.init()
    cwd = getcwd()
    ui_font = pygame.font.Font(
        os.path.join(base_path, "ui", "font.ttf"), 24 * globals.ui_scale
    )
    title_font = pygame.font.Font(
        os.path.join(base_path, "ui", "font.ttf"), 64 * globals.ui_scale
    )

    menubg = pygame.image.load(os.path.join(base_path, "ui", "menu.png"))
    game_title = title_font.render("Souls Of Metal", fontalias, primary)
    game_logo = pygame.image.load(
        os.path.join(base_path, "ui", "logo.png")
    ).convert_alpha()

    current_menu = Menu.MAIN_MENU
    tick = 0
    mouse_pressed = False

    sprites = pygame.sprite.Group()

    major_country_select = MajorCountrySelect(
        os.path.join(base_path, "starts", "Modern World", "majors.txt"),
        5,
        ui_font,
        sprites,
    )
    minor_country_select = MinorCountrySelect(
        os.path.join(base_path, "starts", "Modern World", "minors.txt"), 5, sprites
    )
    with open(
        os.path.join(base_path, "CountryData.json")
    ) as f:  # REMEMBER NOT TO USE HARDCODED PATH -minh-
        countries_data = load(f)
    countries = Countries(countries_data)
    map = Map("Modern World", (0, 0), 1)

    player_country = None

    selected_country_rgb = 0

    menubuttons = [
        Button("Start Game", (200, 400), (160, 40), 5),
        Button("Continue Game", (200, 500), (160, 40), 5),
        Button("Settings", (200, 600), (160, 40), 5),
        Button("Credits", (200, 700), (160, 40), 5),
        Button("Exit", (200, 800), (160, 40), 5),
    ]

    settingsbuttons = [
        Button("UI Size", (200, 200), (160, 40), 5),
        Button("FPS", (200, 300), (160, 40), 5),
        Button("Sound Volume", (200, 400), (160, 40), 5),
        Button("Music Volume", (200, 500), (160, 40), 5),
        Button("Scroll Invert", (200, 600), (160, 40), 5),
        Button("Save Settings", (200, 800), (160, 40), 5),
        Button("Exit", (200, 900), (160, 40), 5),
    ]

    countryselectbuttons = [
        Button("Back", (1125, 570), (160, 40), 5),
        Button("Map Select", (1375, 570), (160, 40), 5),
        Button("Country List", (1125, 670), (160, 40), 5),
        Button("Start", (1375, 670), (160, 40), 5),
    ]

    mapbuttons = [
        Button("Diplomacy", (65, 25), (120, 40), 5),
        Button("Building", (195, 25), (120, 40), 5),
        Button("Military", (325, 25), (120, 40), 5),
        Button("Estates ", (455, 25), (120, 40), 5),
        Button("-", (770, 25), (40, 40), 5),
        Button("+", (1150, 25), (40, 40), 5),
        # NOTE(soi): oh so thats why buttons should have ids
        Button(display_date, (960, 25), (320, 40), 5),
    ]

    escapemenubuttons = [
        Button("Resume", (200, 400), (160, 40), 5),
        Button("Back to Main Menu", (200, 500), (160, 40), 5),
        Button("Settings", (200, 600), (160, 40), 5),
    ]

    division_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    division_target = division_pos

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
                        case pygame.K_ESCAPE:
                            if current_menu == Menu.CREDITS:
                                current_menu = Menu.MAIN_MENU
                            if current_menu == Menu.GAME:
                                current_menu = Menu.ESCAPEMENU

                case pygame.MOUSEWHEEL:
                    # mouse_pressed = True
                    mouse_scroll = -settings_json["Scroll Invert"] * event.y

                    if current_menu == Menu.COUNTRY_SELECT:
                        major_country_select.update(mouse_scroll)
                        major_country_select.scroll -= mouse_scroll
                        major_country_select.scroll = func.clamp(
                            major_country_select.scroll,
                            0,
                            len(major_country_select.majors) - 5,
                        )
                        major_country_select.min = major_country_select.scroll
                        major_country_select.max = min(
                            len(major_country_select.majors),
                            6 + major_country_select.scroll,
                        )
                    elif current_menu == Menu.GAME:
                        map.scale = func.clamp(map.scale - (mouse_scroll / 25), 1, 2)
                        map.cvmap = pygame.transform.scale_by(map.cmap, map.scale)
                        map.pos[0] = -mouse_pos[0] * (map.scale - 1)
                        map.pos[1] = -mouse_pos[1] * (map.scale - 1)

                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pressed = True
                        r, g, b, _ = screen.get_at(pygame.mouse.get_pos())
                        selected_country_rgb = (r, g, b)
                        division_target = pygame.Vector2(mouse_pos)

                case pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_pressed = False

                case pygame.K_ESCAPE:
                    if event.button == 1:
                        current_menu = Menu.MAIN_MENU

        if current_menu != Menu.GAME:
            screen.blit(menubg, (0, 0))

            if current_menu == Menu.ESCAPEMENU:  # Why can't I use != :sob:
                surface = pygame.Surface((screen.get_width(), screen.get_height()))
                surface.set_alpha(180)
                surface.fill((0, 0, 0))
                screen.blit(surface, (0, 0))
                for button in escapemenubuttons:
                    hovered = button.draw(
                        screen, mouse_pos, mouse_pressed, settings_json, tick, ui_font
                    )
                    if not mouse_pressed or not hovered:
                        continue

                    mouse_pressed = False  # Eat input

                    match button.id:
                        case "Resume":
                            current_menu = Menu.GAME
                        case "Back to main menu":
                            current_menu = Menu.MAIN_MENU
                        case "Setting":
                            current_menu = Menu.SETTINGS
            elif current_menu == Menu.MAIN_MENU:
                screen.blit(game_title, (400, 160))

                screen.blit(game_logo, (30, 30))

                for button in menubuttons:
                    hovered = button.draw(
                        screen, mouse_pos, mouse_pressed, settings_json, tick, ui_font
                    )
                    if not mouse_pressed or not hovered:
                        continue

                    # NOTE(pol): Eat input
                    mouse_pressed = False

                    match button.id:
                        case "Settings":
                            current_menu = Menu.SETTINGS
                        case "Start Game":
                            current_menu = Menu.COUNTRY_SELECT
                        case "Credits":
                            current_menu = Menu.CREDITS
                        case "Exit":
                            global_run = False

            elif current_menu == Menu.SETTINGS:
                for button in settingsbuttons:
                    hovered = button.draw(
                        screen, mouse_pos, mouse_pressed, settings_json, tick, ui_font
                    )

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
                            with open(
                                os.path.join(base_path, "settings.json"), "w"
                            ) as f:
                                dump(settings_json, f)

                        case "Exit":
                            current_menu = Menu.MAIN_MENU

            elif current_menu == Menu.COUNTRY_SELECT:
                # pygame.draw.rect(screen, (50, 50, 50), ((300, 40), (1200, 1000)), 0, 20)
                # pygame.draw.rect(screen, (40, 40, 40), ((1000, 540), (500, 200)), 0, 20)
                sprites.draw(screen)
                pygame.draw.rect(
                    major_country_select.image,
                    (40, 40, 40),
                    ((00, 0), (700 * globals.ui_scale, 180 * globals.ui_scale)),
                    0,
                    20,
                )

                country_height = 0
                for major in major_country_select.majors[
                    major_country_select.min : major_country_select.max :
                ]:
                    major.pos[1] = country_height
                    country_height += 200
                    # NOTE(soi): there has to be a better wat to handle this
                    hovered = major.draw(
                        major_country_select.image,
                        (
                            mouse_pos[0] - major_country_select.rect[0][0],
                            mouse_pos[1] - major_country_select.rect[0][1],
                        ),
                        player_country,
                        mouse_pressed,
                    )
                    if not mouse_pressed or not hovered:
                        continue

                    player_country = major.id

                for minor in minor_country_select.minors[
                    minor_country_select.min : minor_country_select.max :
                ]:
                    hovered = minor.draw(
                        minor_country_select.image,
                        mouse_pos,
                        player_country,
                        mouse_pressed,
                    )
                    if not mouse_pressed or not hovered:
                        continue
                    player_country = minor.id

                for button in countryselectbuttons:
                    hovered = button.draw(
                        screen, mouse_pos, mouse_pressed, settings_json, tick, ui_font
                    )
                    if not mouse_pressed or not hovered:
                        continue

                    match button.id:
                        case "Start":
                            current_menu = Menu.GAME
                        case "Back":
                            current_menu = Menu.MAIN_MENU
            elif current_menu == Menu.CREDITS:
                screen.fill((0, 0, 0))
                font = pygame.font.Font(
                    os.path.join(base_path, "ui", "font.ttf"), 36 * globals.ui_scale
                )
                lines = [
                    "                                                                       Souls Of Metal",
                    "                                                                       Original Creator: 123456",
                    "                                                     Developer(s): 123456789, 1234567890, 12345678",
                    "                                                                       Tester(s): 1234567",
                    "",
                    "                                                                       Thanks for Playing! :3",
                ]
                for i, line in enumerate(lines):
                    text = font.render(line, True, (255, 255, 255))
                    screen.blit(text, (100, 100 + i * 50))

        else:
            delta = division_target - division_pos
            if delta.length() > 1:
                division_pos += delta.normalize()

            map.draw(screen, mouse_rel)
            # NOTE(soi): definitely should hv this in like Map's draw and fix how its being placed

            pygame.draw.circle(screen, secondary, division_pos, 5)
            # print(selected_country_rgb)
            if selected_country_rgb in countries.colorsToCountries:
                pygame.draw.rect(
                    screen,
                    tertiary,
                    pygame.Rect((-10, 15), (625, 1065)),
                    border_bottom_right_radius=64,
                    border_top_right_radius=64,
                )
                pygame.draw.rect(
                    screen,
                    secondary,
                    pygame.Rect((-10, 15), (625, 1065)),
                    border_bottom_right_radius=64,
                    border_top_right_radius=64,
                    width=10,
                )
                country = countries.colorsToCountries[selected_country_rgb]
                screen.blit(
                    countries.countriesToFlags[country],
                    (30, 85),
                )
                screen.blit(
                    title_font.render(
                        globals.language_translations[country],
                        fontalias,
                        primary,
                    ),
                    (30, 300),
                )
            for button in mapbuttons:
                hovered = button.draw(
                    screen, mouse_pos, mouse_pressed, settings_json, tick, ui_font
                )
                if not mouse_pressed or not hovered:
                    continue
                match button.id:
                    case "-":
                        speed = max(speed - 1, 0)
                    case "+":
                        speed = min(speed + 1, 7)
                # NOTE(soi): i feel like we should indicate time based on the day night map thing
            if (not tick % ((8 - speed) * 10)) and speed:
                date += datetime.timedelta(days=1)
                display_date = date.strftime("%A, %B %e, %Y")
                # NOTE(soi): theres probably a better way to do this
                mapbuttons[-1].id = display_date

        tick += 1

        pygame.time.Clock().tick(settings_json["FPS"])
        pygame.display.update()


main()
