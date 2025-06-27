import pygame

def lerp(i, f, t, slow = 5):
    return int( (i * (1 - ( t/slow )) + (f * t/slow)) if t/slow < 1 else f )

def round_corners(surface, radius):
    radius *=3
    # Create a new surface with the same size as the input surface, but with an alpha channel
    rounded_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    
    # Draw the corners with arcs
    pygame.draw.circle(rounded_surface,(255, 255, 255), (radius, radius), radius )
    pygame.draw.circle(rounded_surface,(255, 255, 255), (surface.get_width() - radius , radius ), radius )
    pygame.draw.circle(rounded_surface,(255, 255, 255), (radius , surface.get_height() - radius ), radius )
    pygame.draw.circle(rounded_surface,(255, 255, 255), (surface.get_width() - radius , surface.get_height() - radius ), radius )
    
    # Fill the rest of the surface
    pygame.draw.rect(rounded_surface, (255, 255, 255), (radius, 0, surface.get_width() - 2 * radius, surface.get_height()))
    pygame.draw.rect(rounded_surface, (255, 255, 255), (0, radius, surface.get_width(), surface.get_height() - 2 * radius))
    
    # Use the mask to combine the original surface with the new surface with rounded corners
    surface.blit(rounded_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    
    return surface
