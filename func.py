import pygame
from pygame.transform import scale


def clamp(value, a, b):
    return max(min(value, b), a)


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
