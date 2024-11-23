from utils import get_max_dimension
import pygame
import math
CURRENT_MAX_DIMENSION = get_max_dimension()
TILE_WIDTH = 16
TILE_HEIGHT = 16
VIEW_PORT_TILES_W = 32
VIEW_PORT_TILES_H = 32
pygame.init()
SCREEN = pygame.display.set_mode(
 (CURRENT_MAX_DIMENSION - 1 / 6 * CURRENT_MAX_DIMENSION,
  CURRENT_MAX_DIMENSION - 1 / 6 * CURRENT_MAX_DIMENSION)
)
SCALE_FACTOR = math.ceil(CURRENT_MAX_DIMENSION / TILE_WIDTH / VIEW_PORT_TILES_W)
SCREEN_WIDTH = SCREEN.get_width()
SCREEN_HEIGHT = SCREEN.get_height()