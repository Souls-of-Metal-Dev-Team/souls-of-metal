import pygame


def clamp(value, a, b):
    return max(min(value, b), a)


# If you change this function the ui breaks for some reason
def lerp(v0, v1, t):
    return v0 * (1 - t) + v1 * t


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
