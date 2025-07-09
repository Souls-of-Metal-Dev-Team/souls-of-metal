import pygame
import random
from CountryData import Countries
from func import outline, clamp
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

global music_index
music_tracks = ["FDJ.mp3", "Lenin is young again.mp3", "Katyusha.mp3", "Soilad 62.mp3"]
music_index = 0

base_path = os.path.dirname(__file__)
if getattr(sys, "frozen", False):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

Menu = Enum("Menu", "MAIN_MENU COUNTRY_SELECT SETTINGS CREDITS GAME ESCAPEMENU")
pygame.display.set_caption("Soul Of Steel")
icon = pygame.image.load(os.path.join(base_path, "ui", "logo.png"))
pygame.display.set_icon(icon)


def main():
    global music_index
    speed = 0
    sidebar_tab = ""
    sidebar_pos = -625

    chara_desc = pygame.Rect((0, 0), (200, 200))

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
    screen = pygame.display.set_mode((1920, 1080), pygame.DOUBLEBUF | pygame.SCALED, vsync=1)

    pygame.mixer.init()

    # Load music

    # NOTE(soi):i meant shuffle as in play a random song next after a song is over smsmsmsh
    SONG_FINISHED = pygame.USEREVENT + 1
    # NOTE(soi): ehhhhhhhhh
    pygame.mixer.music.set_endevent(SONG_FINISHED)
    music_tracks = os.listdir(os.path.join(base_path, "sound", "music"))
    music_path = random.choice(music_tracks)
    random.shuffle(music_tracks)
    if os.path.exists(os.path.join(base_path, "sound", "music", music_path)):
        print(music_path)
        pygame.mixer.music.load(os.path.join(base_path, "sound", "music", music_path))
        pygame.mixer.music.set_volume(0.5)

        pygame.mixer.music.play(0)
    else:
        print("[WARNING] Music file not found at:", music_path)
    with open(os.path.join(base_path, "translation.json")) as f:
        globals.language_translations = load(f)

    # NOTE(soi): kepping this at game for debugging reasons
    current_menu = Menu.GAME
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
    with open(os.path.join(base_path, "province-centers.json")) as f:
        province_centers = load(f)

    globals.ui_scale = settings_json["UI Size"] // 14

    pygame.font.init()
    cwd = getcwd()
    ui_font = pygame.font.Font(os.path.join(base_path, "ui", "font.ttf"), 24 * globals.ui_scale)
    title_font = pygame.font.Font(os.path.join(base_path, "ui", "font.ttf"), 64 * globals.ui_scale)

    menubg = pygame.image.load(os.path.join(base_path, "ui", "menu.png"))
    game_title = title_font.render("Souls Of Metal", fontalias, primary)
    game_logo = pygame.image.load(os.path.join(base_path, "ui", "logo.png")).convert_alpha()

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
    scaled_maps = [pygame.transform.scale_by(map.cmap, i) for i in range(1, 11)]
    player_country = None

    selected_country_rgb = 0

    menubuttons = [
        Button("Start Game", (200, 400), (160, 40), 5, settings_json, ui_font),
        Button("Continue Game", (200, 500), (160, 40), 5, settings_json, ui_font),
        Button("Settings", (200, 600), (160, 40), 5, settings_json, ui_font),
        Button("Credits", (200, 700), (160, 40), 5, settings_json, ui_font),
        Button("Exit", (200, 800), (160, 40), 5, settings_json, ui_font),
    ]

    settingsbuttons = [
        Button("UI Size", (200, 200), (160, 40), 5, settings_json, ui_font),
        Button("FPS", (200, 300), (160, 40), 5, settings_json, ui_font),
        Button("Sound Volume", (200, 400), (160, 40), 5, settings_json, ui_font),
        Button("Music Volume", (200, 500), (160, 40), 5, settings_json, ui_font),
        Button(
            f"Music: {music_tracks[music_index]}", (200, 600), (160, 40), 5, settings_json, ui_font
        ),
        Button("Scroll Invert", (200, 700), (160, 40), 5, settings_json, ui_font),
        Button("Save Settings", (200, 800), (160, 40), 5, settings_json, ui_font),
        Button("Exit", (200, 900), (160, 40), 5, settings_json, ui_font),
    ]

    countryselectbuttons = [
        Button("Back", (1125, 570), (160, 40), 5, settings_json, ui_font),
        Button("Map Select", (1375, 570), (160, 40), 5, settings_json, ui_font),
        Button("Country List", (1125, 670), (160, 40), 5, settings_json, ui_font),
        Button("Start", (1375, 670), (160, 40), 5, settings_json, ui_font),
    ]

    mapbuttons = [
        Button("/:diplo Diplomacy", (65, 25), (120, 40), 5, settings_json, ui_font),
        Button("Building", (195, 25), (120, 40), 5, settings_json, ui_font),
        Button("Military", (325, 25), (120, 40), 5, settings_json, ui_font),
        Button("Estates ", (455, 25), (120, 40), 5, settings_json, ui_font),
        Button("-", (770, 25), (40, 40), 5, settings_json, ui_font),
        Button("+", (1150, 25), (40, 40), 5, settings_json, ui_font),
        # NOTE(soi): oh so thats why buttons should have ids
        Button(display_date, (960, 25), (320, 40), 5, settings_json, ui_font),
    ]

    escapemenubuttons = [
        Button("Resume", (200, 400), (160, 40), 5, settings_json, ui_font),
        Button("Settings", (200, 600), (160, 40), 5, settings_json, ui_font),
        Button("Back to Main Menu", (200, 500), (160, 40), 5, settings_json, ui_font),
    ]

    division_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    division_target = division_pos

    camera_pos = pygame.Vector2()

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
                        major_country_select.scroll = clamp(
                            major_country_select.scroll,
                            0,
                            len(major_country_select.majors) - 5,
                        )
                        major_country_select.min = major_country_select.scroll
                        major_country_select.max = min(
                            len(major_country_select.majors),
                            6 + major_country_select.scroll,
                        )
                    # elif current_menu == Menu.GAME:
                    #     map.scale = func.clamp(map.scale - (mouse_scroll / 12), 1, 3)
                    #     map.cvmap = pygame.transform.scale_by(map.cmap, map.scale)
                    #     map.pos[0] = -mouse_pos[0] * (map.scale - 1)
                    #     map.pos[1] = -mouse_pos[1] * (map.scale - 1)

                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pressed = True

                case pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_pressed = False

                case pygame.K_ESCAPE:
                    if event.button == 1:
                        current_menu = Menu.MAIN_MENU
            # NOTE(soi): this doesnt woek in the match statement and idk why
            if event.type == SONG_FINISHED:
                music_path = random.choice(music_tracks)
                random.shuffle(music_tracks)
                if os.path.exists(os.path.join(base_path, "sound", "music", music_path)):
                    print(music_path)
                    pygame.mixer.music.load(os.path.join(base_path, "sound", "music", music_path))
                    pygame.mixer.music.set_volume(0.5)

                    pygame.mixer.music.play(0)
                else:
                    print("[WARNING] Music file not found at:", music_path)

        screen.fill((0, 0, 0))
        if current_menu != Menu.GAME:
            screen.blit(menubg, (0, 0))

        match current_menu:
            case Menu.ESCAPEMENU:  # Why can't I use != :sob:
                surface = pygame.Surface((screen.get_width(), screen.get_height()))
                surface.set_alpha(180)
                surface.fill((0, 0, 0))
                screen.blit(surface, (0, 0))
                for button in escapemenubuttons:
                    hovered = button.draw(screen, mouse_pos, mouse_pressed, tick)
                    if not mouse_pressed or not hovered:
                        continue

                    mouse_pressed = False  # Eat input

                    match button.id:
                        case "Resume":
                            current_menu = Menu.GAME
                        case "Settings":
                            current_menu = Menu.SETTINGS
                        case "Back to Main Menu":
                            current_menu = Menu.MAIN_MENU

            case Menu.MAIN_MENU:
                screen.blit(game_title, (400, 160))

                screen.blit(game_logo, (30, 30))

                for button in menubuttons:
                    hovered = button.draw(screen, mouse_pos, mouse_pressed, tick)
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

            case Menu.SETTINGS:
                for button in settingsbuttons:
                    hovered = button.draw(screen, mouse_pos, mouse_pressed, tick)

                    if not hovered:
                        continue

                        # Handle dynamic music ID (e.g., "Music: 1.mp3")
                        if button.id.startswith("Music:") and mouse_pressed and hovered:
                            music_index = (music_index + 1) % len(music_tracks)
                            music_path = os.path.join(
                                base_path, "sound", "music", music_tracks[music_index]
                            )
                            try:
                                pygame.mixer.music.load(music_path)
                                pygame.mixer.music.set_volume(settings_json["Music Volume"] / 100)
                                pygame.mixer.music.play(-1)
                                print("Now playing:", music_tracks[music_index])
                                settings_json["Music Track"] = music_index
                                button.id = f"Music: {music_tracks[music_index]}"
                            except Exception as e:
                                print("[ERROR] Failed to play music:", e)
                            mouse_pressed = False

                        else:
                            match button.id:
                                case "UI Size":
                                    settings_json["UI Size"] += mouse_scroll
                                    settings_json["UI Size"] = func.clamp(
                                        settings_json["UI Size"], 14, 40
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
                            settings_json["Scroll Invert"] = clamp(
                                settings_json["Scroll Invert"], 0, 1
                            )
                            settings_json["Scroll Invert"] = settings_json["Scroll Invert"] * -2 + 1

                        case "Save Settings":
                            with open(os.path.join(base_path, "settings.json"), "w") as f:
                                dump(settings_json, f)

                        case "Exit":
                            current_menu = Menu.MAIN_MENU

            case Menu.COUNTRY_SELECT:
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
                    hovered = button.draw(screen, mouse_pos, mouse_pressed, tick)
                    if not mouse_pressed or not hovered:
                        continue

                    match button.id:
                        case "Start":
                            current_menu = Menu.GAME
                        case "Back":
                            current_menu = Menu.MAIN_MENU
            case Menu.CREDITS:
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

            case Menu.GAME:
                # WASD + Arrow key camera movement
                keys = pygame.key.get_pressed()
                direction = pygame.Vector2(0, 0)
                move_speed = 10 / map.scale

                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    direction.y = -1
                if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    direction.y = 1
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    direction.x = -1
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    direction.x = 1

                if direction.length_squared() > 0:
                    direction = direction.normalize()
                    camera_pos += direction * move_speed

                # Credit: https://stackoverflow.com/a/20791835
                mouse_world_pos = (pygame.Vector2(mouse_pos) + camera_pos) / map.scale

                # Zoom
                map.scale += mouse_scroll
                map.scale = clamp(map.scale, 2, 10)

                camera_pos = mouse_world_pos * map.scale - pygame.Vector2(mouse_pos)

                # Panning
                mouse_sensitivity = 1 / 5
                match pygame.mouse.get_pressed():
                    case (_, 1, _):
                        camera_pos.x -= mouse_rel[0] * mouse_sensitivity
                        camera_pos.y -= mouse_rel[1] * mouse_sensitivity

                scaled_map = scaled_maps[map.scale - 1]
                map_rect = scaled_map.get_rect()
                map_rect.x -= int(camera_pos.x)
                map_rect.y -= int(camera_pos.y)
                # NOTE(pol): Do not reenable this I will crash out. It breaks zoom.
                # Clamp the camera_pos directly!
                # map_rect.y = func.clamp(
                #     map_rect.y - int(camera_pos.y), 1080 - map_rect.height, 0
                # )

                # Render map
                # screen.blit(scaled_map, map_rect.topleft)
                screen.blit(scaled_map, (map_rect.x % scaled_map.get_width(), map_rect.y))
                screen.blit(
                    scaled_map,
                    (
                        (map_rect.x % scaled_map.get_width()) - scaled_map.get_width(),
                        map_rect.y,
                    ),
                )

                # Get selected country
                hovered = map_rect.collidepoint(mouse_pos)
                # NOTE(soi): I should fix the part whre it lags frm zoom
                if hovered and mouse_pressed:
                    coord = pygame.Vector2(mouse_pos) - pygame.Vector2(map_rect.topleft)
                    pixel = pygame.Vector2()
                    pixel.x = coord.x * map.cmap.get_width() / map_rect.width
                    pixel.y = coord.y * map.cmap.get_height() / map_rect.height
                    r, g, b, _ = map.cmap.get_at((int(pixel.x), int(pixel.y)))
                    selected_country_rgb = (r, g, b)

                    pixel.x = coord.x * map.pmap.get_width() / map_rect.width
                    pixel.y = coord.y * map.pmap.get_height() / map_rect.height
                    r, g, b, _ = map.pmap.get_at((int(pixel.x), int(pixel.y)))
                    selected_province_id = f"{r}, {g}, {b}"
                    print("selected country :", selected_province_id)
                    print(sidebar_tab)
                    if selected_country_rgb != (0, 0, 0):
                        sidebar_tab = (
                            "Diplomacy"
                            if selected_country_rgb in countries.colorsToCountries.keys()
                            else ""
                        )
                        center = province_centers[selected_province_id]
                        division_target = pygame.Vector2(center)
                    else:
                        sidebar_tab = ""

                delta = division_target - division_pos
                division_speed = 10
                if delta.length() > 10:
                    division_pos += delta.normalize() * division_speed
                else:
                    division_pos = division_target

                # Transform coord relative to map to screen coord
                division_screen_pos = pygame.Vector2()
                division_screen_pos.x = division_pos.x * map_rect.width / map.cmap.get_width()
                division_screen_pos.y = division_pos.y * map_rect.height / map.cmap.get_height()
                division_screen_pos += map_rect.topleft

                # Draw division
                pygame.draw.circle(screen, secondary, division_screen_pos, 5)

                # print(selected_country_rgb)
                pygame.draw.rect(
                    screen,
                    tertiary,
                    pygame.Rect((sidebar_pos, 15), (625, 1065)),
                    border_bottom_right_radius=64,
                    border_top_right_radius=64,
                )
                pygame.draw.rect(
                    screen,
                    secondary,
                    pygame.Rect((sidebar_pos, 15), (625, 1065)),
                    border_bottom_right_radius=64,
                    border_top_right_radius=64,
                    width=10,
                )
                if sidebar_tab:
                    sidebar_pos = min(sidebar_pos + 45, -10)
                    match sidebar_tab:
                        # NOTE(soi): this feels inneficient
                        case "Diplomacy":
                            if selected_country_rgb in countries.colorsToCountries:
                                country = countries.colorsToCountries[selected_country_rgb]
                                countrystats = countries.countryData[country][-1]
                                screen.blit(
                                    countries.countriesToFlags[country],
                                    (80 + sidebar_pos, 85),
                                )
                                screen.blit(
                                    ui_font.render(
                                        f"Political power:{countrystats[0]}",
                                        fontalias,
                                        primary,
                                    ),
                                    (150 + sidebar_pos, 480),
                                )
                                screen.blit(
                                    ui_font.render(
                                        f"Stability:{countrystats[1]}",
                                        fontalias,
                                        primary,
                                    ),
                                    (150 + sidebar_pos, 510),
                                )
                                screen.blit(
                                    ui_font.render(
                                        f"Money:{countrystats[2]}",
                                        fontalias,
                                        primary,
                                    ),
                                    (150 + sidebar_pos, 540),
                                )
                                screen.blit(
                                    ui_font.render(
                                        f"Manpower:{countrystats[3]}",
                                        fontalias,
                                        primary,
                                    ),
                                    (150 + sidebar_pos, 570),
                                )
                                if country in countries.Characters:
                                    # NOTE(soi): im doing this bcuz the characters get rendered on top of the character decription (theres probably a better way of doing this)
                                    for i, character in reversed(
                                        list(
                                            enumerate(countries.Display_Characters[country].keys())
                                        )
                                    ):
                                        screen.blit(character, (120 * i + sidebar_pos + 80, 255))
                                        if character.get_rect(
                                            left=120 * i + sidebar_pos + 80, top=255
                                        ).collidepoint(mouse_pos):
                                            chara_desc.left, chara_desc.top = mouse_pos

                                            pygame.draw.rect(
                                                screen,
                                                tertiary,
                                                chara_desc,
                                                border_radius=16,
                                            )
                                            pygame.draw.rect(
                                                screen,
                                                secondary,
                                                chara_desc,
                                                border_radius=16,
                                                width=4,
                                            )
                                            for i, trait in enumerate(
                                                countries.Characters[country][character]
                                            ):
                                                if ":" not in trait:
                                                    screen.blit(
                                                        ui_font.render(
                                                            trait.split(".")[1]
                                                            .replace("=", "")
                                                            .capitalize(),
                                                            fontalias,
                                                            secondary,
                                                        ),
                                                        (
                                                            mouse_pos[0] + 15,
                                                            mouse_pos[1] + 30 * i + 15,
                                                        ),
                                                    )
                                                else:
                                                    screen.blit(
                                                        ui_font.render(
                                                            trait[6::],
                                                            fontalias,
                                                            primary,
                                                        ),
                                                        (
                                                            mouse_pos[0] + 15,
                                                            mouse_pos[1] + 30 * i + 15,
                                                        ),
                                                    )
                                screen.blit(
                                    outline(
                                        title_font.render(
                                            globals.language_translations[country],
                                            fontalias,
                                            primary,
                                        ),
                                        7,
                                        tertiary,
                                    ),
                                    (150 + sidebar_pos, 350),
                                )
                        case _:
                            print("uhoh")

                            sidebar_pos = max(sidebar_pos - 45, -625)

                else:
                    sidebar_pos = max(sidebar_pos - 45, -625)
                for button in mapbuttons:
                    hovered = button.draw(screen, mouse_pos, mouse_pressed, tick)
                    if not mouse_pressed or not hovered:
                        continue
                    match button.id:
                        case "-":
                            speed = max(speed - 1, 0)
                        case "+":
                            speed = min(speed + 1, 7)
                        case "Diplomacy":
                            # NOTE(soi): should turn this into an enum someday
                            sidebar_tab = "Diplomacy"
                        case "Military":
                            sidebar_tab = "Military"

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
