import pygame
from classes import ButtonDraw, fontalias, primary, secondary, tertiary
import globals

THICCMAX = 5


def draw_button(screen: pygame.Surface, mouse_pos: tuple[int, int], button_draw: ButtonDraw):
    pos = button_draw.pos.to_tuple()
    size = button_draw.size.to_tuple()
    button = button_draw.button
    text = button_draw.text or button.string
    text_font = button_draw.text_font

    rect = pygame.Rect(pos, size)

    hovered = pygame.Rect.collidepoint(rect, mouse_pos)

    if hovered:
        if button.thicc < THICCMAX:
            button.thicc += 1
    else:
        button.thicc = max(button.thicc - 1, 0)

    scaled_thicc = button.thicc * globals.ui_scale

    if scaled_thicc:
        pygame.draw.rect(
            screen,
            secondary,
            pygame.Rect(
                rect.x - scaled_thicc,
                rect.y - scaled_thicc,
                rect.width + scaled_thicc * 2,
                rect.height + scaled_thicc * 2,
            ),
            border_radius=rect.height * scaled_thicc // 2,
        )

    pygame.draw.rect(screen, tertiary, rect, border_radius=rect.height)

    if button.image:
        screen.blit(
            button.image,
            (
                rect.centerx - button.image.get_width() / 2,
                rect.y,
            ),
        )

    if text and text_font:
        text_color = secondary if hovered else primary
        text_surface: pygame.Surface = text_font.render(text, fontalias, text_color)
        screen.blit(
            text_surface,
            (
                rect.centerx - text_surface.get_width() / 2,
                rect.y + (THICCMAX * globals.ui_scale),
            ),
        )

    return hovered
