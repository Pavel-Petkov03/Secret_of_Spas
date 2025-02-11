import pygame

pygame.init()

VALID_RESOLUTIONS = [
    1536,
    1280,
    1024,
    768,
    512,
]


def get_max_dimension():
    display_info = pygame.display.Info()
    native_width, native_height = display_info.current_w, display_info.current_h
    current_max_dim = min(native_height, native_width)
    for resolution in VALID_RESOLUTIONS:
        if resolution < current_max_dim:
            return resolution
