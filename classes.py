from pygame import draw, Rect, font, Surface, sprite, transform, image
from os import getcwd
from json import load
import pygame
from func import lerp,round_corners

with open("translation.json") as json_data:
    trans = load(json_data)

with open("theme.json") as json_data:
    theme = load(json_data)
    primary = tuple(theme["primary"])
    secondary = tuple(theme["secondary"])
    tertiary = tuple(theme["tertiary"])
    fontalias = theme["fontalias"]

with open("settings.json") as json_data:
    uiscale = int(load(json_data)["UI Size"] / 14)

cwd = getcwd()

font.init()
font = font.Font(f"{cwd}/ui/font.ttf", 24 * uiscale)


class Button:
    thicc = 0
    i = 0
    def __init__(self, id, pos, dim, thicc):
        self.id = id
        self.pos = pos
        self.dim = dim
        self.thiccmax = thicc
        self.mouse_up = False
        self.brect = Rect(
            self.pos[0] - (self.dim[0] * uiscale >> 1),
            self.pos[1],
            self.dim[0] * uiscale,
            self.dim[1] * uiscale,
        )

    def draw(self, screen, mpos, mtogg, settings_json,tick):
        self.thicc = lerp(self.thicc,self.thiccmax if Rect.collidepoint(self.brect, mpos) else 0,tick-self.i)
        if not Rect.collidepoint(self.brect, mpos):
            self.i = tick
        draw.rect(
            screen,
            secondary,
            Rect(
                self.pos[0] - (self.dim[0] * uiscale >> 1),
                self.pos[1] - (self.thicc * uiscale),
                self.dim[0] * uiscale,
                self.dim[1] * uiscale + (self.thicc * uiscale << 1),
            ),
        )
        draw.circle(
            screen,
            secondary,
            (
                self.pos[0] - (self.dim[0] * uiscale >> 1),
                self.pos[1] + (self.dim[1] * uiscale >> 1),
            ),
            (self.dim[1] * uiscale >> 1) + self.thicc * uiscale,
        )
        draw.circle(
            screen,
            secondary,
            (
                self.pos[0] + (self.dim[0] * uiscale >> 1),
                self.pos[1] + (self.dim[1] * uiscale >> 1),
            ),
            (self.dim[1] * uiscale >> 1) + self.thicc * uiscale,
        )

        draw.rect(
            screen,
            tertiary,
            self.brect,
        )
        draw.circle(
            screen,
            tertiary,
            (
                self.pos[0] - (self.dim[0] * uiscale >> 1),
                self.pos[1] + (self.dim[1] * uiscale >> 1),
            ),
            (self.dim[1] * uiscale >> 1),
        )
        draw.circle(
            screen,
            tertiary,
            (
                self.pos[0] + (self.dim[0] * uiscale >> 1),
                self.pos[1] + (self.dim[1] * uiscale >> 1),
            ),
            (self.dim[1] * uiscale >> 1),
        )

        text = (
            f"{trans[self.id]}: {settings_json[self.id]}"
            if self.id in settings_json
            else self.id
        )
        font_render = font.render(
            text,
            fontalias,
            secondary if Rect.collidepoint(self.brect, mpos) and mtogg else primary,
        )
        screen.blit(
            font_render,
            (
                self.pos[0] - (font_render.get_width() >> 1),
                self.pos[1] + (self.thiccmax * uiscale),
            ),
        )

        if Rect.collidepoint(self.brect, mpos) and mtogg:
            return self.id


class MajorCountrySelect(sprite.Sprite):
    def __init__(self, file, thicc, *groups):
        super().__init__(*groups)
        self.majors = []
        count = 0
        with open(file) as f:
            for k in f.read().split(", "):
                self.majors.append(MajorCountry(k, (0, count), thicc))
                count += 200
        self.image = Surface((700, 1000), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 0))
        self.rect = ((300, 40), (700, 1000))
        self.min = min([k.pos[1] for k in self.majors])
        self.max = max([k.pos[1] for k in self.majors]) + 200

    def update(self):
        self.min = min([k.pos[1] for k in self.majors])
        self.max = max([k.pos[1] for k in self.majors]) + 200


class MajorCountry:
    def __init__(self, id, pos, thicc):
        self.id = id
        self.pos = pos
        self.thicc = thicc

        try:
            self.img = image.load(f'flags/{self.id.lower()}_flag.png').convert_alpha()
        except FileNotFoundError:
            self.img = image.load('unknown.jpg').convert_alpha()

        h = self.img.get_height()
        scale = ( 180 - ( thicc <<1))/h 
        self.img = round_corners( transform.scale_by(self.img,scale) ,5)
        self.w,h = self.img.get_size()
        self.mouse_up = False
        self.brect = Rect(
            self.pos[0],
            self.pos[1],
            700 * uiscale,
            200 * uiscale,
        )

    def draw(self, screen, mpos, select, mtogg):
        draw.rect(screen, tertiary, ((self.pos[0], self.pos[1]), (700, 180)), 0, 20)
        draw.rect(screen, secondary, ((self.pos[0], self.pos[1]), (700, 180)), 5, 20)
        font_render = font.render(
            trans[self.id],
            fontalias,
            (
                secondary
                if (Rect.collidepoint(self.brect, mpos) and mtogg) or select == self.id
                else primary
            ),
        )
        screen.blit(self.img, (self.pos[0] + (self.thicc), self.pos[1]+5 ))
        screen.blit(font_render, (self.pos[0] + 25 + self.w, self.pos[1] + 25))
        if Rect.collidepoint(self.brect, mpos) and mtogg:
            return self.id
