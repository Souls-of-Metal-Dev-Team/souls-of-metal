import os
from json import load
import pygame
from pygame.rect import Rect
from pygame.transform import scale
from func import round_corners, clamp
import globals

base_path = os.path.dirname(__file__)

cwd = os.getcwd()
with open(os.path.join(base_path, "theme.json")) as f:
    theme = load(f)
    primary = tuple(theme["primary"])
    secondary = tuple(theme["secondary"])
    tertiary = tuple(theme["tertiary"])
    fontalias = theme["fontalias"]


class Button:
    # last_tick = 0

    def __init__(self, id, pos, size, thicc):
        self.id = id
        self.thicc = 0
        self.thiccmax = thicc
        # NOTE(soi): uhh poleve yk u cant just multiply like this right?
        # scaled_size = pygame.Vector2(size * globals.ui_scale)
        # print(globals.ui_scale)
        scaled_size = [i * globals.ui_scale for i in size]
        # NOTE(soi): might fuck up some buttons widths but idc i want my buttonsto ble like my women
        # R O T U N D
        # scaled_size[0] += 2 * scaled_size[1]
        self.rect = pygame.Rect((0, 0), scaled_size)
        # NOTE(soi): yea pygame already has a thing for centering rects, should read the documentation more smsmsmh
        self.rect.center = (pos[0], pos[1])

    def draw(self, screen, mouse_pos, mouse_pressed, settings_json, tick, ui_font):
        _ = tick

        hovered = pygame.Rect.collidepoint(self.rect, mouse_pos)

        if hovered:
            if self.thicc < self.thiccmax:
                self.thicc += 1
                # self.thicc = lerp(
                #     self.thicc,
                #     self.thiccmax,
                #     (tick - self.last_tick) / 5,
                # )
        else:
            self.thicc = max(self.thicc - 1, 0)
            # self.last_tick = tick

        scaled_thicc = self.thicc * globals.ui_scale

        if scaled_thicc:
            pygame.draw.rect(
                screen,
                secondary,
                pygame.Rect(
                    self.rect.x - scaled_thicc,
                    self.rect.y - scaled_thicc,
                    self.rect.width + scaled_thicc * 2,
                    self.rect.height + scaled_thicc * 2,
                ),
                border_radius=self.rect.height * scaled_thicc // 2,
            )
        # pygame.draw.circle(
        #     screen,
        #     secondary,
        #     (self.rect.x, self.rect.centery),
        #     self.rect.height / 2 + scaled_thicc,
        # )
        # pygame.draw.circle(
        #     screen,
        #     secondary,
        #     (
        #         self.rect.right,
        #         self.rect.centery,
        #     ),
        #     self.rect.height / 2 + scaled_thicc,
        # )

        pygame.draw.rect(screen, tertiary, self.rect, border_radius=self.rect.height)
        # pygame.draw.circle(
        #     screen,
        #     tertiary,
        #     (
        #         self.rect.x,
        #         self.rect.centery,
        #     ),
        #     self.rect.height / 2,
        # )
        # pygame.draw.circle(
        #     screen,
        #     tertiary,
        #     (
        #         self.rect.right,
        #         self.rect.centery,
        #     ),
        #     self.rect.height / 2,
        # )

        text = (
            f"{globals.language_translations[self.id]}: {settings_json[self.id]}"
            if self.id in settings_json
            else self.id
        )
        text_surface = ui_font.render(
            text, fontalias, secondary if hovered and mouse_pressed else primary
        )
        screen.blit(
            text_surface,
            (
                self.rect.centerx - text_surface.get_width() / 2,
                self.rect.y + (self.thiccmax * globals.ui_scale),
            ),
        )

        return hovered


class MajorCountrySelect(pygame.sprite.Sprite):
    def __init__(self, file, thicc, ui_font, *groups):
        super().__init__(*groups)
        self.min = 0
        self.max = 6
        self.majors = []
        count = 0
        with open(file) as f:
            for k in f.read().split(", "):
                self.majors.append(MajorCountry(k, [0, count], thicc, ui_font))
                count += 200
        # print(len(self.majors))
        self.image = pygame.Surface((700, 1000), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 0))
        self.rect = ((300, 40), (700, 1000))
        self.scroll = 0


class MajorCountry:
    def __init__(self, id, pos, thicc, ui_font):
        self.id = id
        self.pos = pos
        self.thiccmax = self.thicc = thicc * globals.ui_scale

        try:
            self.img = pygame.image.load(
                f"flags/{self.id.lower()}_flag.png"
            ).convert_alpha()
        except FileNotFoundError:
            self.img = pygame.image.load(
                os.path.join(base_path, "unknown.jpg")
            ).convert_alpha()

        h = self.img.get_height()
        scale = (180 - (thicc << 1)) / h
        self.img = round_corners(pygame.transform.scale_by(self.img, scale), 5)
        self.w, h = self.img.get_size()
        self.mouse_up = False
        self.selected_font_render = ui_font.render(
            globals.language_translations[self.id],
            fontalias,
            secondary,
        )
        self.font_render = ui_font.render(
            globals.language_translations[self.id],
            fontalias,
            primary,
        )

    def draw(self, screen, mouse_pos, select, mouse_pressed):
        # NOTE(soi): pygames rect has an update function and idk if i should implement it here
        brect = pygame.Rect(
            self.pos[0],
            self.pos[1],
            700 * globals.ui_scale,
            180 * globals.ui_scale,
        )
        # NOTE(soi): yayyyy animationssss :DDDD
        if pygame.Rect.collidepoint(brect, mouse_pos) or select == self.id:
            if self.thicc < self.thiccmax:
                self.thicc += 1
        else:
            self.thicc = max(self.thicc - 1, 1)
            # self.last_tick = tick
        pygame.draw.rect(screen, tertiary, brect, 0, 20)
        screen.blit(self.img, (self.pos[0] + (self.thicc), self.pos[1] + 5))
        if (
            (pygame.Rect.collidepoint(brect, mouse_pos) and mouse_pressed)
            or select == self.id
            or self.thicc > 1
        ):
            pygame.draw.rect(screen, tertiary, brect, 2 * self.thicc, 20)
            screen.blit(
                self.selected_font_render, (self.pos[0] + 25 + self.w, self.pos[1] + 25)
            )
        else:
            screen.blit(self.font_render, (self.pos[0] + 25 + self.w, self.pos[1] + 25))
        pygame.draw.rect(screen, secondary, brect, 5, 20)
        return pygame.Rect.collidepoint(brect, mouse_pos) and mouse_pressed


class MinorCountrySelect(pygame.sprite.Sprite):
    min = 0
    max = 32

    def __init__(self, file, thicc, *groups):
        super().__init__(*groups)
        self.minors = []
        count = 0
        with open(file) as f:
            for k in f.read().split(", "):
                self.minors.append(
                    MinorCountry(k, [count % 4 * 100 + 50, count // 4 * 60 + 15], thicc)
                )
                count += 1
        if len(self.minors) > 32:
            self.minors = self.minors[0:32]

        self.image = pygame.Surface((500, 500), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 0))
        self.rect = ((1000, 40), (200, 1000))

    def update(self, scroll):
        # self.min = 3
        # self.max = 8
        self.min = scroll
        self.max = min(len(self.minors), 6 + scroll)
        print(self.min, self.max)


class MinorCountry:
    def __init__(self, id, pos, thicc):
        self.id = id
        self.pos = pos
        self.thicc = self.thiccmax = thicc

        try:
            self.img = pygame.image.load(
                f"flags/{self.id.lower()}_flag.png"
            ).convert_alpha()
        except FileNotFoundError:
            self.img = pygame.image.load(
                os.path.join(base_path, "unknown.jpg")
            ).convert_alpha()

        h = self.img.get_height()
        scale = (180 - (thicc << 1)) / h / 4
        self.img = round_corners(pygame.transform.scale_by(self.img, scale), 3)
        self.w, self.h = self.img.get_size()
        self.mouse_up = False
        self.brect = pygame.Rect(
            self.pos[0],
            self.pos[1],
            self.w,
            self.h,
        )

    def draw(self, screen, mpos, select, mtogg):
        b = pygame.Rect(
            self.pos[0] + 1000,
            self.pos[1] + 40,
            self.w,
            self.h,
        )
        # NOTE(soi): hopefully me moving around the code alot for animations doesnt mess anything up
        screen.blit(self.img, (self.pos[0], self.pos[1]))
        if pygame.Rect.collidepoint(b, mpos) or select == self.id:
            if self.thicc < self.thiccmax:
                self.thicc += 1
            pygame.draw.rect(
                screen, tertiary, self.brect, border_radius=9, width=self.thicc
            )
            pygame.draw.rect(
                screen, secondary, self.brect, border_radius=9, width=self.thicc // 2
            )
        else:
            self.thicc = max(self.thicc - 2, 1)

        return pygame.Rect.collidepoint(b, mpos) and mtogg


class Map:
    # sidebar = pygame.image.load(os.path.join(base_path, "ui", "sidebar.png")).convert()

    def __init__(self, scenario, pos, scale):
        self.scale = scale
        self.pos = pygame.Vector2(pos)
        self.cmap = self.cvmap = pygame.image.load(
            os.path.join(base_path, "starts", scenario, "map.png")
        ).convert()
        self.pmap = pygame.image.load(
            os.path.join(base_path, "starts", scenario, "province.png")
        ).convert()
        self.pmap = pygame.transform.scale_by(self.pmap, 1080 / self.cmap.get_height())
        self.cmap = pygame.transform.scale_by(self.cmap, 1080 / self.cmap.get_height())
        self.cvmap = pygame.transform.scale_by(self.cmap, self.scale)

    def draw(self, screen, rel):
        match pygame.mouse.get_pressed():
            case (_, 1, _):
                self.pos[0] = self.pos[0] + rel[0] / (5 * self.scale)
                self.pos[1] = clamp(
                    (self.pos[1] + rel[1] / (5 * self.scale)),
                    -1080 * (self.scale - 1),
                    0,
                )
        screen.blit(self.cvmap, ((self.pos[0] % 1920), self.pos[1]))
        screen.blit(self.cvmap, (((self.pos[0]) % 1920) - 1920, self.pos[1]))
