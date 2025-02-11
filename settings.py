from utils.max_resolution_helper import get_max_dimension
import pygame

CURRENT_MAX_DIMENSION = get_max_dimension()
TILE_WIDTH = 16
TILE_HEIGHT = 16
VIEW_PORT_TILES_W = 32
VIEW_PORT_TILES_H = 32
pygame.init()
TILES = 100
MAP_WIDTH = TILE_WIDTH * TILES
MAP_HEIGHT = TILE_HEIGHT * TILES

SCREEN_WIDTH = CURRENT_MAX_DIMENSION - 1 / 8 * CURRENT_MAX_DIMENSION
SCREEN_HEIGHT = CURRENT_MAX_DIMENSION - 1 / 8 * CURRENT_MAX_DIMENSION
SCALE_FACTOR = SCREEN_HEIGHT / TILE_WIDTH / VIEW_PORT_TILES_H


VILLAGE_URL = "village"

PLAYER_POS_DUNGEON_LOGGER = {
    "first_level": (700, 500),
    VILLAGE_URL: (1100, 0)
}

GATE_LEVEL_INFO = {
    "first_level": {
        "village_name": "Rakiq dungeon",
        "village_image_location": "src/images/dungeon_pictures/first_dungeon.png"
    }
}
