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
    "first_level": (700, 0),
    VILLAGE_URL: (1100, 0),
    "second_level": (250, 1100),
    "third_level": (0, 900),
    "fourth_level": (320, 0),
}

GATE_LEVEL_INFO = {
    VILLAGE_URL: {
        "village_name": "Village",
        "village_image_location": "src/images/dungeon_pictures/village.png"
    },
    "first_level": {
        "village_name": "Rakiq dungeon",
        "village_image_location": "src/images/dungeon_pictures/first_dungeon.png"
    },
    "second_level": {
        "village_name": "Gin dungeon",
        "village_image_location": "src/images/dungeon_pictures/second_dungeon.png"
    },
    "third_level": {
        "village_name": "Wine dungeon",
        "village_image_location": "src/images/dungeon_pictures/third_dungeon.png"
    },
    "fourth_level": {
        "village_name": "Vodka dungeon",
        "village_image_location": "src/images/dungeon_pictures/fourth_dungeon.png"
    }
}
