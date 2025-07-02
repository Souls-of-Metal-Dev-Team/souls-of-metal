import pygame
import os
import sys
from json import load, dump
from enum import Enum
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
    screen,
)

# Robust base path (works when run from .exe too)
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

Menu = Enum("Menu", "main_menu countryselect settings game credits")

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

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((1920, 1080), pygame.DOUBLEBUF | pygame.SCALED, vsync=1)

    # Load music
    music_path = os.path.join(base_path, "sound", "music", "background.mp3")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    else:
        print("[WARNING] Music file not found at:", music_path)

    menubg = pygame.image.load(os.path.join(base_path, "ui", "menu.png"))
    game_title = title_font.render("Souls Of Metal", fontalias, primary)
    game_logo = pygame.image.load(os.path.join(base_path, "ui", "logo.png")).convert_alpha()

    try:
        with open(os.path.join(base_path, "settings.json")) as json_data:
            settings_json = load(json_data)
    except FileNotFoundError:
        settings_json = {
            "Scroll Invert": -1,
            "UI Size": 14,
            "FPS": 139,
            "Sound Volume": 0,
            "Music Volume": 0,
        }
        with open(os.path.join(base_path, "settings.json"), "w") as json_data:
            dump(settings_json, json_data)

    scrollinvert = settings_json["Scroll Invert"]
    tick = 0
    mouse_pressed = False
    mouse_scroll = 0
    tab = [1]
    current_menu = Menu.main_menu
    player_country = None
    selected_country = 0

    sprites = pygame.sprite.Group()
    countrymajor = MajorCountrySelect(os.path.join(base_path, "starts", "Modern World", "majors.txt"), 5, sprites)
    countryminor = MinorCountrySelect(os.path.join(base_path, "starts", "Modern World", "minors.txt"), 5, sprites)
    selectmenu = CountryMenu()
    with open(os.path.join(base_path, "CountryData.json")) as json_data:
        countries_data = load(json_data)
    countries = Countries(countries_data)
    map = Map("Modern World")

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
                        case pygame.K_ESCAPE:
                            if current_menu == Menu.credits:
                                current_menu = Menu.main_menu
                case pygame.MOUSEWHEEL:
                    mouse_pressed = True
                    mouse_scroll = -scrollinvert * event.y
                    if current_menu == Menu.countryselect:
                        countrymajor.update(mouse_scroll)
                    elif current_menu == Menu.game:
                        map.update(mouse_scroll, mpos)
                case pygame.MOUSEBUTTONDOWN:
                    mouse_pressed = True
                    mouse_scroll = 0
                    r, g, b, _ = screen.get_at(pygame.mouse.get_pos())
                    selected_country = (r, g, b)
                case pygame.MOUSEBUTTONUP | pygame.MOUSEMOTION:
                    mouse_pressed = False
                    mouse_scroll = 0

        if current_menu != Menu.game:
            screen.blit(menubg, (0, 0))

            if current_menu == Menu.main_menu:
                screen.blit(game_title, (400, 160))
                screen.blit(game_logo, (30, 30))
                for i in menubuttons:
                    temp = i.draw(screen, mpos, mouse_pressed, settings_json, tick)
                    if temp:
                        tab = temp
                match tab:
                    case "Settings": current_menu = Menu.settings
                    case "Start Game": current_menu = Menu.countryselect
                    case "Credits": current_menu = Menu.credits
                    case "Exit": global_run = False
                tab = 0

            elif current_menu == Menu.credits:
                screen.fill((0, 0, 0))
                font = pygame.font.SysFont("arial", 36)
                lines = [
                    "Souls Of Metal",
                    "Created by: Your Name",
                    "Thanks to: Pygame, OpenAI",
                    "",
                    "Press ESC to return"
                ]
                for i, line in enumerate(lines):
                    text = font.render(line, True, (255, 255, 255))
                    screen.blit(text, (100, 100 + i * 50))

            elif current_menu == Menu.settings:
                for i in settingsbuttons:
                    temp = i.draw(screen, mpos, mouse_pressed, settings_json, tick)
                    if temp:
                        tab = temp
                match tab:
                    case "Exit": current_menu = Menu.main_menu
                    case "UI Size":
                        settings_json["UI Size"] = func.clamp(settings_json["UI Size"] + mouse_scroll, 14, 40)
                    case "Scroll Invert":
                        settings_json["Scroll Invert"] = func.clamp(settings_json["Scroll Invert"], 0, 1)
                        settings_json["Scroll Invert"] = settings_json["Scroll Invert"] * -2 + 1
                    case "Sound Volume":
                        settings_json["Sound Volume"] = func.clamp(settings_json["Sound Volume"] + mouse_scroll, 0, 100)
                    case "Music Volume":
                        settings_json["Music Volume"] = func.clamp(settings_json["Music Volume"] + mouse_scroll, 0, 100)
                        pygame.mixer.music.set_volume(settings_json["Music Volume"] * 0.01)
                    case "FPS":
                        settings_json["FPS"] = max(settings_json["FPS"] + mouse_scroll, 12)
                with open(os.path.join(base_path, "settings.json"), "w") as json_data:
                    dump(settings_json, json_data)
                mouse_pressed = False
                tab = 0

            elif current_menu == Menu.countryselect:
                sprites.draw(screen)
                pygame.draw.rect(countrymajor.image, (40, 40, 40), ((0, 0), (700, 1000)), 0, 20)
                for i, major in enumerate(countrymajor.majors[countrymajor.min:countrymajor.max]):
                    major.pos[1] = i * 200
                    temp = major.draw(countrymajor.image, mpos, player_country, mouse_pressed)
                    if temp:
                        player_country = temp
                for minor in countryminor.minors[countryminor.min:countryminor.max]:
                    temp = minor.draw(countryminor.image, mpos, player_country, mouse_pressed)
                    if temp:
                        player_country = temp
                for i in countryselectbuttons:
                    temp = i.draw(screen, mpos, mouse_pressed, settings_json, tick)
                    if temp:
                        tab = temp
                match tab:
                    case "Start": current_menu = Menu.game
                    case "Back": current_menu = Menu.main_menu
                tab = 0

        else:
            map.draw(screen, pygame.mouse.get_rel())
            if selected_country in countries.colorsToCountries:
                selectmenu.draw(screen, countries, countries.colorsToCountries[selected_country])

        tick += 1
        pygame.time.Clock().tick(settings_json["FPS"])
        pygame.display.update()

main()
