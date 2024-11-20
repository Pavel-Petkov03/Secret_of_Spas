import math
import pygame
from pytmx.util_pygame import load_pygame

pygame.init()
display_info = pygame.display.Info()
native_width, native_height = display_info.current_w, display_info.current_h
tile_width = 16
tile_height = 16
VIEW_PORT_TILES_W = 32
VIEW_PORT_TILES_H = 32
current_max_dim = min(native_height, native_width)
scale_factor = math.ceil(current_max_dim / tile_width / VIEW_PORT_TILES_W)
screen = pygame.display.set_mode((current_max_dim - 1 / 6 * current_max_dim, current_max_dim - 1 / 6 * current_max_dim))
tmx_data = load_pygame("src/tiles/level_1.tmx")
current_start_pos_x = 100
current_start_pos_y = 100
print(scale_factor)



def get_tile_properties(x, y, layer):
    if layer and hasattr(layer, 'tiles'):
        gid = layer.data[y][x]

        properties = tmx_data.get_tile_properties_by_gid(gid)
        return properties
    return None


for gid, image in enumerate(tmx_data.images):
    if image is not None:
        new_width = image.get_width() * scale_factor
        new_height = image.get_height() * scale_factor
        scaled_image = pygame.transform.scale(image, (new_width, new_height))
        tmx_data.images[gid] = scaled_image

circle_surface = pygame.Surface((30 * 2, 30 * 2), pygame.SRCALPHA)
pygame.draw.circle(circle_surface, (255, 0, 0), (5 * 2, 5 * 2), 5 * 2)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        current_start_pos_x = current_start_pos_x - 0.7
    if keys[pygame.K_RIGHT]:
        current_start_pos_x = current_start_pos_x + 0.7
    if keys[pygame.K_UP]:
        current_start_pos_y = current_start_pos_y - 0.7
    if keys[pygame.K_DOWN]:
        current_start_pos_y = current_start_pos_y + 0.7

    center_x = screen.get_width() / 2
    center_y = screen.get_width() / 2
    for layer in tmx_data.visible_layers:
        if hasattr(layer, "tiles"):
            for x, y, tile in layer.tiles():

                if current_start_pos_x - tile_width <= x * tile_width <= current_start_pos_x + VIEW_PORT_TILES_W * tile_width + tile_width \
                        and current_start_pos_y - tile_width <= y * tile_height <= current_start_pos_y + VIEW_PORT_TILES_H * tile_height + tile_width:
                    screen_x = (x * tile_width - current_start_pos_x) * scale_factor
                    screen_y = (y * tile_height - current_start_pos_y) * scale_factor
                    screen.blit(tile, (screen_x, screen_y))

    screen.blit(circle_surface, (center_x, center_y))
    screen.blit(circle_surface, (current_start_pos_x, current_start_pos_y))
    pygame.display.update()
    pygame.display.flip()

pygame.quit()
