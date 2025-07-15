import pygame
<<<<<<< HEAD
import pygame.gfxdraw
from pygame.transform import scale
from math import cos, sin
import numpy as np


# def gkern(kernlen=21, std=3):
#     gkern1d = signal.gaussian(kernlen, std=std).reshape(kernlen, 1)
#     gkern2d = np.outer(gkern1d, gkern1d)
#     return gkern2d


def changeestates(estates: dict, change: dict) -> dict:
    for k, v in change.items():
        estates[k] += v
    total_influence = sum(estates.values())
    return {k: v / total_influence for k, v in estates.items()}


def gkern(l=5, sig=1.0):
    """\
    creates gaussian kernel with side length `l` and a sigma of `sig`
    """
    ax = np.linspace(-(l - 1) / 2.0, (l - 1) / 2.0, l)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return pygame.mask.from_surface(
        pygame.surfarray.make_surface(kernel / np.sum(kernel)), threshold=254
    )


def outline(surface, thicc, color):
    convolution_mask = pygame.mask.Mask((thicc, thicc), fill=True)
    convolution_mask.set_at((0, 0), value=0)
    convolution_mask.set_at((thicc - 1, 0), value=0)
    convolution_mask.set_at((0, thicc - 1), value=0)
    convolution_mask.set_at((thicc - 1, thicc - 1), value=0)
    convolution_mask = gkern(thicc)
    mask = pygame.mask.from_surface(surface)
    outline_surface = mask.convolve(convolution_mask).to_surface(
        setcolor=color, unsetcolor=surface.get_colorkey()
    )
    outline_surface.blit(surface, (thicc // 2, thicc // 2))
    return outline_surface


def glow(surface, thicc, color):
    b = pygame.Surface(
        (surface.get_width() + (4 * thicc), surface.get_height() + (4 * thicc)),
        flags=pygame.SRCALPHA,
    )
    a = b.copy()
    b.blit(surface, (2 * thicc, 2 * thicc))
    pygame.transform.gaussian_blur(b, thicc, dest_surface=a)
    a.fill(color, special_flags=pygame.BLEND_RGBA_MIN)
    a.blit(surface, (2 * thicc, 2 * thicc), special_flags=pygame.BLEND_RGBA_ADD)
    return a


def shadow(surface, thicc, color):
    b = pygame.Surface(
        (surface.get_width() + 4 * thicc, surface.get_height() + 4 * thicc), flags=pygame.SRCALPHA
    )
    a = b.copy()
    b.blit(surface, (2 * thicc, 2 * thicc))
    pygame.transform.gaussian_blur(b, thicc, dest_surface=a)
    a.fill(color, special_flags=pygame.BLEND_RGBA_MIN)
    a.blit(surface, (2 * thicc, 2 * thicc))
    return a

<<<<<<< HEAD
=======
>>>>>>> 53967ea (Remove some useless things.)
=======
>>>>>>> 9f5f475 (added functions tht shadow and glow a surface)

def clamp(value, a, b):
    return max(min(value, b), a)

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 9f5f475 (added functions tht shadow and glow a surface)

def pichart(screen, pos, radius, percentages):
    start_angle = 0
    for percent in percentages.values():
        pygame.draw.polygon(
            screen,
            percent[0],
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 031214d (uhhhh)
            [
                pygame.math.Vector2(pos),
                *[
                    pos + radius * pygame.math.Vector2(cos(i * 0.0174527), sin(i * 0.0174527))
                    for i in range(start_angle, round(percent[1] * 360))
                ],
<<<<<<< HEAD
=======
            [pygame.math.Vector2(pos)]
            + [
                pos + radius * pygame.math.Vector2(cos(i * 0.0174527), sin(i * 0.0174527))
                for i in range(start_angle, round(percent[1] * 360))
>>>>>>> 540e33f (made pi charts work better)
=======
>>>>>>> 031214d (uhhhh)
            ],
        )
        start_angle = round(percent[1] * 360)


def compass(screen, pos, line_colour, point_colour, compass_axis, tick, country_ideology):
    country_ideology /= 100
    x_right = pygame.math.Vector2(cos(tick), -sin(tick) / (2**0.5)) * 100 + pos
    x_left = pygame.math.Vector2(-cos(tick), sin(tick) / (2**0.5)) * 100 + pos
    y_right = pygame.math.Vector2(-sin(tick), -cos(tick) / (2**0.5)) * 100 + pos
    y_left = pygame.math.Vector2(sin(tick), cos(tick) / (2**0.5)) * 100 + pos
    z_right = pygame.math.Vector2(0, 1 / (2**0.5)) * 100 + pos
    z_left = pygame.math.Vector2(0, -1 / (2**0.5)) * 100 + pos
    projected_pos = (
        pygame.math.Vector2(
            country_ideology[0] * cos(tick) - country_ideology[1] * sin(tick),
            -1
            / (2**0.5)
            * (
                (country_ideology[1] * cos(tick))
                + (country_ideology[0] * sin(tick))
                - country_ideology[2]
            ),
        )
        * 100
        + pos
    )
    pygame.draw.aaline(screen, line_colour, x_right, x_left)
    pygame.draw.aaline(screen, line_colour, y_right, y_left)
    pygame.draw.aaline(screen, line_colour, z_right, z_left)
    pygame.draw.circle(screen, point_colour, projected_pos, 5)
    screen.blit(compass_axis[0], x_right + (2, 0))
    screen.blit(compass_axis[1], x_left + (2, 0))
    screen.blit(compass_axis[2], y_right + (2, 0))
    screen.blit(compass_axis[3], y_left + (2, 0))
    screen.blit(compass_axis[4], z_right + (2, 6))
    screen.blit(compass_axis[5], z_left + (2, -24))


# If you change this function the ui breaks for some reason
=======
>>>>>>> 53967ea (Remove some useless things.)
def lerp(v0, v1, t):
    return v0 * (1 - t) + v1 * t


def truncate(text, trunc_length):
    return text if len(text) < trunc_length else text[:trunc_length:] + "..."

<<<<<<< HEAD
<<<<<<< HEAD
=======
def outline(surface, thicc, color):
    convolution_mask = pygame.mask.Mask((thicc, thicc), fill=True)
    convolution_mask.set_at((0, 0), value=0)
    convolution_mask.set_at((thicc - 1, 0), value=0)
    convolution_mask.set_at((0, thicc - 1), value=0)
    convolution_mask.set_at((thicc - 1, thicc - 1), value=0)
    mask = pygame.mask.from_surface(surface)
    outline_surface = mask.convolve(convolution_mask).to_surface(
        setcolor=color, unsetcolor=surface.get_colorkey()
    )
    outline_surface.blit(surface, (thicc // 2, thicc // 2))
    return outline_surface

>>>>>>> 53967ea (Remove some useless things.)
=======
>>>>>>> 9f5f475 (added functions tht shadow and glow a surface)

def round_corners(surface, radius):
    radius *= 3
    # Create a new surface with the same size as the input surface, but with an alpha channel
    rounded_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

    pygame.draw.rect(
        rounded_surface,
        (255, 255, 255),
        (0, 0, surface.get_width(), surface.get_height()),
        border_radius=radius,
    )

    # Use the mask to combine the original surface with the new surface with rounded corners
    surface.blit(rounded_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    return surface
