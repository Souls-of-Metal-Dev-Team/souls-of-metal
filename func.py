import pygame
from pygame.transform import scale
from math import cos, sin


def clamp(value, a, b):
    return max(min(value, b), a)


def compass(screen, pos, tick):
    position = pygame.math.Vector2(100, 500)
    x_right = pygame.math.Vector2(cos(tick), -sin(tick) / (2**0.5)) * 100 + position
    x_left = pygame.math.Vector2(-cos(tick), sin(tick) / (2**0.5)) * 100 + position
    y_right = pygame.math.Vector2(-sin(tick), -cos(tick) / (2**0.5)) * 100 + position
    y_left = pygame.math.Vector2(sin(tick), cos(tick) / (2**0.5)) * 100 + position
    z_right = pygame.math.Vector2(0, 1 / (2**0.5)) * 100 + position
    z_left = pygame.math.Vector2(0, -1 / (2**0.5)) * 100 + position
    projected_pos = (
        pygame.math.Vector2(
            pos[0] * cos(tick) - pos[1] * sin(tick),
            -1 / (2**0.5) * ((pos[1] * cos(tick)) + (pos[0] * sin(tick)) - pos[2]),
        )
        * 100
        + position
    )
    pygame.draw.line(screen, (255, 255, 255), x_right, x_left)
    pygame.draw.line(screen, (255, 255, 255), y_right, y_left)
    pygame.draw.line(screen, (255, 255, 255), z_right, z_left)
    pygame.draw.circle(screen, (255, 0, 127), projected_pos, 5)


# If you change this function the ui breaks for some reason
def lerp(v0, v1, t):
    return v0 * (1 - t) + v1 * t


def truncate(text, trunc_length):
    return text if len(text) < trunc_length else text[:trunc_length:] + "..."


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
