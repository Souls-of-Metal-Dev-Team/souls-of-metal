from pygame import draw, Rect, font
from os import getcwd
from json import load
from settings import uisize, mv, sv, fps

with open("translation.json") as json_data:
    trans = load(json_data)

with open("theme.json") as json_data:
    theme = load(json_data)
    primary = tuple(theme["primary"])
    secondary = tuple(theme["secondary"])
    tertiary = tuple(theme["tertiary"])
    fontalias = theme["fontalias"]

cwd = getcwd()

font.init()
font = font.Font(f"{cwd}/ui/font.ttf", 24)


class Button:
    def __init__(self, id, pos, dim, thicc):
        self.id = id
        self.pos = pos
        self.dim = dim
        self.thicc = thicc
        self.c1 = primary
        self.c2 = secondary
        self.c3 = tertiary
        self.mouse_up = False
        self.brect = Rect(
            self.pos[0] - (self.dim[0] >> 1),
            self.pos[1],
            self.dim[0],
            self.dim[1],
        )

    def draw(self, screen, mpos, mtogg, tab, settings_json):
        if Rect.collidepoint(self.brect, mpos):
            draw.rect(
                screen,
                self.c2,
                Rect(
                    self.pos[0] - (self.dim[0] >> 1),
                    self.pos[1] - self.thicc,
                    self.dim[0],
                    self.dim[1] + (self.thicc << 1),
                ),
            )
            draw.circle(
                screen,
                self.c2,
                (self.pos[0] - (self.dim[0] >> 1), self.pos[1] + (self.dim[1] >> 1)),
                (self.dim[1] >> 1) + self.thicc,
            )
            draw.circle(
                screen,
                self.c2,
                (self.pos[0] + (self.dim[0] >> 1), self.pos[1] + (self.dim[1] >> 1)),
                (self.dim[1] >> 1) + self.thicc,
            )

        draw.rect(
            screen,
            self.c3,
            self.brect,
        )
        draw.circle(
            screen,
            self.c3,
            (self.pos[0] - (self.dim[0] >> 1), self.pos[1] + (self.dim[1] >> 1)),
            (self.dim[1] >> 1),
        )
        draw.circle(
            screen,
            self.c3,
            (self.pos[0] + (self.dim[0] >> 1), self.pos[1] + (self.dim[1] >> 1)),
            (self.dim[1] >> 1),
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
            (self.pos[0] - (font_render.get_width() >> 1), self.pos[1] + self.thicc),
        )

        if Rect.collidepoint(self.brect, mpos) and mtogg:
            return self.id
