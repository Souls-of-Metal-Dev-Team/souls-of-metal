from pygame import draw, Rect, font, Surface, mouse, sprite, transform, image
from os import getcwd
from json import load, dump
import pygame
from func import lerp, round_corners, clamp

screen = pygame.display.set_mode(
    (1920, 1080), pygame.DOUBLEBUF | pygame.SCALED, vsync=1
)

with open("translation.json") as json_data:
    trans = load(json_data)

with open("theme.json") as json_data:
    theme = load(json_data)
    primary = tuple(theme["primary"])
    secondary = tuple(theme["secondary"])
    tertiary = tuple(theme["tertiary"])
    fontalias = theme["fontalias"]

settings_json = None

try:
    with open("settings.json") as json_data:
        settings_json = load(json_data)
except FileNotFoundError:
    settings_json = {"Scroll Invert": -1, "UI Size": 14, "FPS": 139, "Sound Volume": 0, "Music Volume": 0}
    with open("settings.json", "w") as json_data:
        dump(settings_json, json_data)

uiscale = int(settings_json["UI Size"] / 14)


cwd = getcwd()

font.init()
# NOTE(pol): Renamed it because it was shadowing font
ui_font = font.Font(f"{cwd}/ui/font.ttf", 24 * uiscale)


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
        font_render = ui_font.render(
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
    min = 0
    max = 6
    def __init__(self, file, thicc, *groups):
        super().__init__(*groups)
        self.majors = []
        count = 0
        with open(file) as f:
            for k in f.read().split(", "):
                self.majors.append(MajorCountry(k, [0, count], thicc))
                count += 200
        print(len(self.majors))
        self.image = Surface((700, 1000), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 0))
        self.rect = ((300, 40), (700, 1000))

    def update(self, scroll):
        # self.min = 3
        # self.max = 8
        self.min = scroll
        self.max = min(len( self.majors ), 6 + scroll)
        print(self.min, self.max)


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
        font_render = ui_font.render(
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


class MinorCountrySelect(sprite.Sprite):
    min = 0
    max = 32

    def __init__(self, file, thicc, *groups):
        super().__init__(*groups)
        self.minors = []
        count = 0
        with open(file) as f:
            for k in f.read().split(", "):
                self.minors.append(MinorCountry(k, [count % 4 * 100 + 50, count // 4 * 60 + 15], thicc))
                count += 1
        if len(self.minors) > 32:
            self.minors = self.minors[0:32]

        print(len(self.minors))
        self.image = Surface((500, 500), pygame.SRCALPHA)
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
        self.thicc = thicc

        try:
            self.img = image.load(f'flags/{self.id.lower()}_flag.png').convert_alpha()
        except FileNotFoundError:
            self.img = image.load('unknown.jpg').convert_alpha()

        h = self.img.get_height()
        scale = (180 - (thicc << 1)) / h / 4
        self.img = round_corners(transform.scale_by(self.img, scale), 3)
        self.w, self.h = self.img.get_size()
        self.mouse_up = False
        self.brect = Rect(
            self.pos[0],
            self.pos[1],
            self.w,
            self.h,
        )

    def draw(self, screen, mpos, select, mtogg):
        b = Rect(
            self.pos[0] + 1000,
            self.pos[1] + 40,
            self.w,
            self.h,
        )
        screen.blit(self.img, (self.pos[0], self.pos[1]))
        if select == self.id:
            draw.rect(screen, secondary, self.brect, border_radius = 9, width= 3)
        if Rect.collidepoint(b, mpos) and mtogg:
            return self.id

class Map:
    sidebar= image.load('ui/sidebar.png').convert()
    scale = 1
    pos = [0,1]
    def __init__(self, scenario):
        self.cmap = self.cvmap = image.load(f'starts/{ scenario }/map.png').convert()
        self.pmap = image.load(f'starts/{ scenario }/province.png').convert()
        self.pmap =  transform.scale_by(self.pmap,1080/self.cmap.get_height())
        self.cmap =  transform.scale_by(self.cmap,1080/self.cmap.get_height())
        self.cvmap =  pygame.transform.scale_by(self.cmap,self.scale)

    def update(self, scroll, mpos):
        self.scale = clamp( self.scale + ( scroll/25 ), 1  ,2)
        self.cvmap =  pygame.transform.scale_by(self.cmap,self.scale)
        self.pos[0] = -mpos[0]*(self.scale-1)
        self.pos[1] = -mpos[1]*(self.scale-1)
    def draw(self,screen, rel):
        match mouse.get_pressed():
            case (_,1,_):
                self.pos[0] = (self.pos[0] + rel[0]/(5*self.scale))
                self.pos[1] = clamp( (self.pos[1] + rel[1]/(5*self.scale)), -1080*(self.scale-1), 0)
        screen.blit(self.cvmap,self.pos)
        pygame.draw.rect(screen,tertiary,( (0,0),(1920,60)))


class CountryMenu():
    def __init__(self):
        pass
    def draw(self,screen):
        draw.rect(screen, tertiary,Rect((-32,-12),(524,1104)), border_radius=64 )
        draw.rect(screen, secondary,Rect((-32,-12),(524,1104)), border_radius=64, width=12 )


