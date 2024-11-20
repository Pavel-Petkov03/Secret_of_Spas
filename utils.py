import pygame

pygame.init()


def get_max_dimension():
    display_info = pygame.display.Info()
    native_width, native_height = display_info.current_w, display_info.current_h
    current_max_dim = min(native_height, native_width)
    return current_max_dim
