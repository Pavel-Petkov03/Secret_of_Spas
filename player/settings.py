from settings import CURRENT_MAX_DIMENSION
from spritesheet.utils import get_animation_matrix
import pygame

PLAYER_ANIMATION_MATRIX = get_animation_matrix("player_movement")
for right_index in (1, 4):
    current_row = list(map(lambda cur: pygame.transform.flip(cur, True, False), PLAYER_ANIMATION_MATRIX[right_index]))
    PLAYER_ANIMATION_MATRIX.append(current_row)
print(len(PLAYER_ANIMATION_MATRIX))
MAIN_PLAYER_NAME = "Kuncho"
MAIN_PLAYER_X_POS = CURRENT_MAX_DIMENSION / 2
MAIN_PLAYER_Y_POS = CURRENT_MAX_DIMENSION / 2
MAIN_PLAYER_HEALTH_POINTS = 100
MAIN_PLAYER_DAMAGE_POINTS = 20
MAIN_PLAYER_CURRENT_ANIMATION_FRAME = PLAYER_ANIMATION_MATRIX[0]
MAIN_PLAYER_ANIMATION_FRAMES = PLAYER_ANIMATION_MATRIX
