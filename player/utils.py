from player.player import Player
import player.settings as settings
from spritesheet.utils import get_animation_matrix
import pygame


def get_main_player_matrix():
    player_matrix = get_animation_matrix("player_movement")
    for right_index in (1, 4):
        current_row = list(map(lambda cur: pygame.transform.flip(cur, True, False), player_matrix[right_index]))
        player_matrix.append(current_row)
    return player_matrix


def init_player(tmx_data):
    player_matrix = get_main_player_matrix()
    return Player(
        settings.MAIN_PLAYER_NAME,
        settings.MAIN_PLAYER_HEALTH_POINTS,
        settings.MAIN_PLAYER_X_POS,
        settings.MAIN_PLAYER_Y_POS,
        settings.MAIN_PLAYER_DAMAGE_POINTS,
        player_matrix[0],
        player_matrix,
        tmx_data
    )
