import pygame
import random
from CountryData import Countries
from func import outline, glow, shadow, clamp, compass, pichart
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
from enum import Enum, auto, IntEnum
import globals
import os
import sys
import datetime
from dataclasses import dataclass, field
from typing import Optional, Any
import networkx as nx

if getattr(sys, "frozen", False):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

THICCMAX = 5

class Menu(Enum):
    MAIN_MENU = auto(),
    COUNTRY_SELECT = auto()
    SETTINGS = auto(),
    CREDITS = auto(),
    GAME = auto(),
    ESCAPEMENU = auto()

class CustomEvents(IntEnum):
    SONG_FINISHED = pygame.USEREVENT+1

@dataclass
class ButtonConfig:
    string: str = ""
    thicc: int = 0
    image: Optional[pygame.Surface] = None

@dataclass
class Vec2i:
    x: int = 0
    y: int = 0
    
    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

@dataclass
class ButtonDraw:
    pos: Vec2i = field(default_factory=Vec2i)
    size: Vec2i = field(default_factory=Vec2i)
    button: ButtonConfig = field(default_factory=ButtonConfig)
    text: Optional[str] = None
    text_font: Optional[pygame.font.Font] = None

def draw_button(screen: pygame.Surface, mouse_pos: tuple[int, int], button_draw: ButtonDraw) -> bool:
    pos = button_draw.pos.to_tuple()
    size = button_draw.size.to_tuple()
    button = button_draw.button
    text = button_draw.text or button.string
    text_font = button_draw.text_font

    rect = pygame.Rect(pos, size)

    hovered = pygame.Rect.collidepoint(rect, mouse_pos)

    if hovered:
        if button.thicc < THICCMAX:
            button.thicc += 1
    else:
        button.thicc = max(button.thicc - 1, 0)

    scaled_thicc = button.thicc * globals.ui_scale

    if scaled_thicc:
        pygame.draw.rect(
            screen,
            secondary,
            pygame.Rect(
                rect.x - scaled_thicc,
                rect.y - scaled_thicc,
                rect.width + scaled_thicc * 2,
                rect.height + scaled_thicc * 2,
            ),
            border_radius=rect.height * scaled_thicc // 2,
        )

    pygame.draw.rect(screen, tertiary, rect, border_radius=rect.height)

    if button.image:
        screen.blit(
            button.image,
            (
                rect.centerx - button.image.get_width() / 2,
                rect.y,
            ),
        )
    
    if text and text_font:
        text_color = secondary if hovered else primary
        text_surface: pygame.Surface = text_font.render(text, fontalias, text_color)
        screen.blit(
            text_surface,
            (
                rect.centerx - text_surface.get_width() / 2,
                rect.y + (THICCMAX * globals.ui_scale),
            ),
        )

    return hovered

def main():
    pygame.display.set_caption("Soul Of Steel")
    icon = pygame.image.load(os.path.join(base_path, "ui", "logo.png"))
    pygame.display.set_icon(icon)

    speed = 0
    sidebar_tab = ""
    sidebar_pos = -625

    music_tracks = ["FDJ.mp3", "Lenin is young again.mp3", "Katyusha.mp3", "Soilad 62.mp3"]
    music_index = 0

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

    # NOTE(soi): kepping this at game for debugging reasons
    current_menu = Menu.GAME
    tick = 0
    mouse_just_pressed = False
    mouse_scroll = 0

    # As you can see you can just initialize settings_json first, this plays nicer with strict typing.

    settings_json: dict[str, Any] = {
        "Scroll Invert": 1,
        "UI Size": 14,
        "FPS": 60,
        "Sound Volume": 50,
        "Music Volume": 50,
        "Music Track": "FDJ"
    }

    try:
        with open(os.path.join(base_path, "settings.json")) as f:
            settings_json = load(f)
    except FileNotFoundError:
        with open(os.path.join(base_path, "settings.json"), "w") as f:
            dump(settings_json, f)

    with open(os.path.join(base_path, "province-centers.json")) as f:
        province_centers = load(f)

    pygame.mixer.music.set_endevent(CustomEvents.SONG_FINISHED)
    music_tracks = os.listdir(os.path.join(base_path, "sound", "music"))
    music_path = random.choice(music_tracks)
    random.shuffle(music_tracks)
    if os.path.exists(os.path.join(base_path, "sound", "music", music_path)):
        pygame.mixer.music.load(os.path.join(base_path, "sound", "music", music_path))
        pygame.mixer.music.set_volume(settings_json["Music Volume"] / 100)

        pygame.mixer.music.play(0)
    else:
        print("[WARNING] Music file not found at:", music_path)
    with open(os.path.join(base_path, "translation.json")) as f:
        globals.language_translations = load(f)
    globals.ui_scale = settings_json["UI Size"] // 14

    pygame.font.init()
    smol_font = pygame.font.Font(os.path.join(base_path, "ui", "font.ttf"), 12 * globals.ui_scale)
    ui_font = pygame.font.Font(os.path.join(base_path, "ui", "font.ttf"), 24 * globals.ui_scale)
    title_font = pygame.font.Font(os.path.join(base_path, "ui", "font.ttf"), 64 * globals.ui_scale)
    compass_axis = (
        smol_font.render("socialism", fontalias, secondary),
        smol_font.render("capitalism", fontalias, secondary),
        smol_font.render("globalism", fontalias, secondary),
        smol_font.render("isolationism", fontalias, secondary),
        smol_font.render("anarchism", fontalias, secondary),
        smol_font.render("authoritarianism", fontalias, secondary),
    )

    menubg = pygame.image.load(os.path.join(base_path, "ui", "menu.png"))
    game_title = glow(title_font.render("Souls Of Metal", fontalias, primary), 5, primary)
    game_logo = glow(
        pygame.image.load(os.path.join(base_path, "ui", "logo.png")).convert_alpha(), 5, primary
    )

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

    with open( os.path.join(base_path, "CountryData.json")) as f:
        countries_data = load(f)
    countries = Countries(countries_data)

    map = Map("Modern World", (0, 0), 1)

    scaled_maps = [pygame.transform.scale_by(map.cmap, i) for i in range(1, 11)]

    player_country = None

    selected_country_rgb = 0

    countryselectbuttons = [
        Button(
            "Back",
            (1125, 570),
            (160, 40),
            5,
            settings_json,
            ui_font,
        ),
        Button(
            "Map Select",
            (1375, 570),
            (160, 40),
            5,
            settings_json,
            ui_font,
        ),
        Button(
            "Country List",
            (1125, 670),
            (160, 40),
            5,
            settings_json,
            ui_font,
        ),
        Button( "Start", (1375, 670), (160, 40), 5, settings_json, ui_font,
        ),
    ]

    mapbuttons = [
        Button("/:diplo Diplomacy", (65, 25), (120, 40), 5, settings_json, ui_font),
        Button("Building", (195, 25), (120, 40), 5, settings_json, ui_font),
        Button("Military", (325, 25), (120, 40), 5, settings_json, ui_font),
        Button("Estates", (455, 25), (120, 40), 5, settings_json, ui_font),
        Button("-", (770, 25), (40, 40), 5, settings_json, ui_font),
        Button("+", (1150, 25), (40, 40), 5, settings_json, ui_font),
        # NOTE(soi): oh so thats why buttons should have ids
        Button(display_date, (960, 25), (320, 40), 5, settings_json, ui_font),
    ]

    with open(os.path.join(base_path, "starts", "Modern World", "neighbors.json")) as json:
        neighbours = {
            eval(k): [tuple(i) for i in v]
            for k, v in load(json).items()
        }
    G = nx.Graph()
    for k, v in neighbours.items():
        for province in v:
            G.add_edge(k, province)

    division_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    division_target = division_pos
    division_path = {}
    division_timer_s = 1.0

    clock = pygame.Clock()

    camera_pos = pygame.Vector2()

    escape_buttons = [
        ButtonConfig("Resume"),
        ButtonConfig("Back to Main Menu"),
        ButtonConfig("Settings")
    ]

    main_menu_buttons = [
        ButtonConfig("Start Game"),
        ButtonConfig("Continue Game"),
        ButtonConfig("Settings"),
        ButtonConfig("Credits"),
        ButtonConfig("Exit")
    ]

    settings_buttons = [
        ButtonConfig("UI Size"),
        ButtonConfig("FPS"),
        ButtonConfig("Sound Volume"),
        ButtonConfig("Music Volume"),

        # NOTE(pol): This draws the track playing but there is no logic for
        # pressing it?
        ButtonConfig("Music"),

        ButtonConfig("Scroll Invert"),
        ButtonConfig("Save Settings"),
        ButtonConfig("Exit")
    ]

    global_run = True
    while global_run:
        mouse_rel = pygame.mouse.get_rel()
        mouse_pos = pygame.mouse.get_pos()
        mouse_scroll = 0
        mouse_just_pressed = False

        for event in pygame.event.get():
            match event.type:
                case CustomEvents.SONG_FINISHED:
                    music_path = random.choice(music_tracks)
                    random.shuffle(music_tracks)
                    if os.path.exists(os.path.join(base_path, "sound", "music", music_path)):
                        pygame.mixer.music.load(
                            os.path.join(base_path, "sound", "music", music_path)
                        )
                        pygame.mixer.music.set_volume(settings_json["Music Volume"] / 100)

                        pygame.mixer.music.play(0)
                    else:
                        print("[WARNING] Music file not found at:", music_path)

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
                    mouse_scroll = settings_json["Scroll Invert"] * event.y

                    if current_menu == Menu.COUNTRY_SELECT:
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

                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_just_pressed = True

                case pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_just_pressed = False

                case _: 
                    pass

        # Clear screen
        screen.fill((0, 0, 0))

        if current_menu != Menu.GAME:
            screen.blit(menubg, (0, 0))

        match current_menu:
            case Menu.ESCAPEMENU:
                # NOTE(pol): This should be a separate asset
                dark_overlay = pygame.Surface((screen.get_width(), screen.get_height()))
                dark_overlay.set_alpha(180)
                dark_overlay.fill((0, 0, 0))
                screen.blit(dark_overlay, (0, 0))

                button_draw = ButtonDraw(
                    size = Vec2i(160, 40),
                    text_font = ui_font
                )

                padding: int = 60
                button_draw.pos = Vec2i(120, screen.get_height()//2 - padding - button_draw.size.y)

                for button in escape_buttons:
                    button_draw.button = button

                    hovered = draw_button(screen, mouse_pos, button_draw)

                    button_draw.pos.y += button_draw.size.y + padding

                    if not mouse_just_pressed or not hovered:
                        continue

                    match button.string:
                        case "Resume":
                            current_menu = Menu.GAME
                        case "Settings":
                            current_menu = Menu.SETTINGS
                        case "Back to Main Menu":
                            current_menu = Menu.MAIN_MENU

            case Menu.MAIN_MENU:
                screen.blit(game_title, (400, 160))
                screen.blit(game_logo, (30, 30))

                button_draw = ButtonDraw(
                    size = Vec2i(160, 40),
                    text_font = ui_font,
                    pos = Vec2i(120, game_logo.get_height() + 30)
                )

                padding: int = 60

                for button in main_menu_buttons:
                    button_draw.button = button

                    hovered = draw_button(screen, mouse_pos, button_draw)
                    button_draw.pos.y += padding + button_draw.size.y

                    if not mouse_just_pressed or not hovered:
                        continue

                    match button.string:
                        case "Settings":
                            current_menu = Menu.SETTINGS
                        case "Start Game":
                            current_menu = Menu.COUNTRY_SELECT
                        case "Credits":
                            current_menu = Menu.CREDITS
                        case "Exit":
                            global_run = False

            case Menu.SETTINGS:
                button_draw = ButtonDraw(
                    size = Vec2i(160, 40),
                    pos = Vec2i(120, 200),
                    text_font = ui_font
                )

                padding: int = 60

                for button in settings_buttons:
                    if button.string in settings_json:
                        button_draw.text = f"{button.string}: {settings_json[button.string]}"
                    elif button.string == "Music":
                        button_draw.text = f"Music: {music_tracks[music_index]}"
                    else:
                        button_draw.text = None

                    button_draw.button = button

                    hovered = draw_button(screen, mouse_pos, button_draw)
                    button_draw.pos.y += padding + button_draw.size.y

                    if not hovered:
                        continue

                    match button.string:
                        case "UI Size":
                            settings_json["UI Size"] += mouse_scroll
                            settings_json["UI Size"] = clamp(settings_json["UI Size"], 14, 40)

                        case "Sound Volume":
                            settings_json["Sound Volume"] += mouse_scroll
                            settings_json["Sound Volume"] = clamp(settings_json["Sound Volume"], 0, 100)

                        case "Music Volume":
                            settings_json["Music Volume"] += mouse_scroll
                            settings_json["Music Volume"] = clamp(settings_json["Music Volume"], 0, 100)
                            pygame.mixer.music.set_volume(settings_json["Music Volume"] / 100)

                        case "FPS":
                            settings_json["FPS"] += mouse_scroll
                            settings_json["FPS"] = clamp(settings_json["FPS"], 12, 999)

                    if not mouse_just_pressed:
                        continue

                    match button.string:
                        case "Scroll Invert":
                            settings_json["Scroll Invert"] *= -1

                        case "Save Settings":
                            with open(os.path.join(base_path, "settings.json"), "w") as f:
                                dump(settings_json, f)

                        case "Exit":
                            if mouse_just_pressed:
                                with open(os.path.join(base_path, "settings.json")) as f:
                                    settings_json = load(f)
                                current_menu = Menu.MAIN_MENU

            case Menu.COUNTRY_SELECT:
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
                        mouse_just_pressed,
                    )
                    if not mouse_just_pressed or not hovered:
                        continue

                    player_country = major.id

                for minor in minor_country_select.minors[
                    minor_country_select.min : minor_country_select.max :
                ]:
                    hovered = minor.draw(
                        minor_country_select.image,
                        mouse_pos,
                        player_country,
                        mouse_just_pressed,
                    )
                    if not mouse_just_pressed or not hovered:
                        continue
                    player_country = minor.id

                for button in countryselectbuttons:
                    hovered = button.draw(screen, mouse_pos, mouse_just_pressed, tick)
                    if not mouse_just_pressed or not hovered:
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
                    "                                                                       Original Creator: Søilad",
                    "                                                     Developer(s): 123456789, 1234567890, 12345678",
                    "                                                                       Tester(s): 1234567",
                    "",
                    "                                                                       Thanks for Playing! :3",
                ]
                for i, line in enumerate(lines):
                    textt: pygame.Surface = font.render(line, True, (255, 255, 255))
                    screen.blit(textt, (100, 100 + i * 50))

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
                map.scale = clamp(map.scale, 1, 10)

                camera_pos = mouse_world_pos * map.scale - pygame.Vector2(mouse_pos)

                # Panning
                mouse_sensitivity = 1
                match pygame.mouse.get_pressed():
                    case (_, 1, _):
                        camera_pos.x -= mouse_rel[0] * mouse_sensitivity
                        camera_pos.y -= mouse_rel[1] * mouse_sensitivity

                scaled_map = scaled_maps[map.scale - 1]
                map_rect = scaled_map.get_rect()
                map_rect.x -= int(camera_pos.x)
                map_rect.y -= int(camera_pos.y)

                screen.fblits(
                    [(scaled_map, (i, map_rect.y)) for i in range(map_rect.x % scaled_map.get_width() - scaled_map.get_width(), 1920, scaled_map.get_width())]
                )

                # Get selected country
                hovered = 0 <= mouse_world_pos.y <= scaled_map.height
                # NOTE(soi): I should fix the part whre it lags frm zoom
                #screen.blit(
                #    ui_font.render(
                #        f"({camera_pos.x:.1f}, {camera_pos.y:.1f}) : ({mouse_world_pos.x:.1f}, {mouse_world_pos.y:.1f}) : ({(mouse_world_pos.x % scaled_map.get_width()):.1f}, {mouse_world_pos.y:.1f})", 
                #        False, 
                #        (255, 255, 255), 
                #        (0, 0, 0)
                #    ), 
                #    (200, 200)
                #)

                if hovered and mouse_just_pressed:
                    coord = mouse_world_pos
                    coord.x %= scaled_map.get_width()
                    r, g, b, _ = map.cmap.get_at((int(coord.x), int(coord.y)))
                    selected_country_rgb = (r, g, b)

                    r, g, b, _ = map.pmap.get_at((int(coord.x), int(coord.y)))
                    selected_province_id = f"{r}, {g}, {b}"
                    if selected_country_rgb != (0, 0, 0):
                        sidebar_tab = ( "Diplomacy" if selected_country_rgb in countries.colorsToCountries.keys() else "")
                        center = province_centers[selected_province_id]
                        division_target = pygame.Vector2(center)

                        division_path = nx.shortest_path(G, source=(0, 1, 0), target=(r, g, b))

                    else:
                        sidebar_tab = ""

                # delta = division_target - division_pos
                # division_speed = 10
                # if delta.length() > 10:
                #     division_pos += delta.normalize() * division_speed
                # else:
                #     division_pos = division_target

                # Transform coord relative to map to screen coord
                division_screen_pos = pygame.Vector2()
                division_screen_pos.x = division_pos.x * map_rect.width / map.cmap.get_width()
                division_screen_pos.y = division_pos.y * map_rect.height / map.cmap.get_height()
                division_screen_pos += map_rect.topleft

                # Draw division
                division_icon = pygame.image.load(os.path.join(base_path, "icons", "plane_icon.png")).convert_alpha()
                division_icon = pygame.transform.smoothscale(division_icon, (24, 24))
                screen.blit(division_icon, division_icon.get_rect(center=division_screen_pos))
                pygame.draw.circle(screen, secondary, division_screen_pos, 5)

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
                        case "Estates":
                            pichart(
                                screen,
                                (150 + sidebar_pos, 200),
                                100,
                                {
                                    "oligarchs": [(255, 90, 189), 0.1],
                                    "proletariat": [(255, 45, 78), 0.2],
                                },
                            )
                        case "Diplomacy":
                            if selected_country_rgb in countries.colorsToCountries:
                                country = countries.colorsToCountries[selected_country_rgb]
                                countrystats = countries.countryData[country][-1]
                                screen.fblits(
                                    [
                                        (
                                            countries.countriesToFlags[country], 
                                            (80 + sidebar_pos, 85)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Political power:{countrystats[0]}",
                                                fontalias,
                                                primary
                                            ), 
                                            (320 + sidebar_pos, 480)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Stability:{countrystats[1]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (320 + sidebar_pos, 510)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Money:{countrystats[2]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (320 + sidebar_pos, 540)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Manpower:{countrystats[3]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (320 + sidebar_pos, 570)
                                        )
                                    ]
                                )
                                compass(
                                    screen,
                                    pygame.math.Vector2(150 + sidebar_pos, 550),
                                    primary,
                                    secondary,
                                    compass_axis,
                                    tick / 100,
                                    pygame.math.Vector3(50, 20, 31.4),
                                )

                                if country in countries.Characters:
                                    # NOTE(soi): im doing this bcuz the characters get rendered on
                                    # top of the character decription (theres probably a better way
                                    # of doing this)
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
                                    shadow(
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
                        case "Military":
                            if selected_country_rgb in countries.colorsToCountries:
                                country = countries.colorsToCountries[selected_country_rgb]
                                countrystats = countries.countryData[country][-1]
                                screen.fblits(
                                    [
                                        (
                                            ui_font.render(
                                                f"Manpower (Reserved):{countrystats[3]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 70)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Manpower (Active):{countrystats[0]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 90)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Manpower (Army):{countrystats[0]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 110)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Tanks:{countrystats[0]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 130)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Motorised:{countrystats[0]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 150)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Manpower (Air force):{countrystats[0]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 170)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Fighters:{countrystats[0]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 190)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Bombers:{countrystats[0]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 210)
                                        ),
                                        (
                                            ui_font.render(
                                                f"CASes:{countrystats[0]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 230)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Manpower (Navy):{countrystats[0]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 250)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Aircraft Carriers:{countrystats[0]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 270)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Battleships:{countrystats[0]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 290)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Destroyer/Brigates:{countrystats[0]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 310)
                                        ),
                                        (
                                            ui_font.render(
                                                f"Medics:{countrystats[0]}",
                                                fontalias,
                                                primary,
                                            ),
                                            (50 + sidebar_pos, 330)
                                        )
                                    ])
                        case _:
                            print("uhoh")

                            sidebar_pos = max(sidebar_pos - 45, -625)

                else:
                    sidebar_pos = max(sidebar_pos - 45, -625)
                for button in mapbuttons:
                    hovered = button.draw(screen, mouse_pos, mouse_just_pressed, tick)
                    if not mouse_just_pressed or not hovered:
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
                        case "Estates":
                            sidebar_tab = "Estates"

                # NOTE(soi): i feel like we should indicate time based on the day night map thing
                if (not tick % ((8 - speed) * 10)) and speed:
                    date += datetime.timedelta(days=1)
                    display_date = date.strftime("%A, %B %e, %Y")
                    # NOTE(soi): theres probably a better way to do this
                    # mapbuttons[-1].id = display_date
                    # NOTE(soi): so this is the better way
                    mapbuttons[-1].hovered_text = ui_font.render(display_date, fontalias, secondary)
                    mapbuttons[-1].normal_text = ui_font.render(display_date, fontalias, primary)

        tick += 1

        division_timer_s -= clock.tick(settings_json["FPS"])/1000.0

        if division_timer_s <= 0:
            print("timeout")
            division_timer_s = 1.0
            if len(division_path) > 0:
                r, g, b = division_path.pop(0)
                division_pos = pygame.Vector2(province_centers[f"{r}, {g}, {b}"])

        pygame.display.update()

main()
