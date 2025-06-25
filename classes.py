from pygame import draw, Rect, font
from os import getcwd
from theme import primary, secondary, tertiary, fontalias

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
        self.brect = Rect(
            self.pos[0] - (self.dim[0] >> 1),
            self.pos[1],
            self.dim[0],
            self.dim[1],
        )

    def draw(self, screen, mpos):
        if Rect.collidepoint(self.brect, mpos):
            draw.rect(
                screen,
                self.c2,
                Rect(
                    self.pos[0] - (self.dim[0] >> 1),
                    self.pos[1] - (self.thicc),
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

        ()
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
        screen.blit(
            font.render(
                self.id,
                fontalias,
                primary if Rect.collidepoint(self.brect, mpos) else secondary,
            ),
            (self.pos[0] - (self.dim[0] >> 1), self.pos[1] + self.thicc),
        )
