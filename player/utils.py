from player.player import Player, Enemy
import player.settings as settings
from spritesheet.utils import get_animation_matrix
import pygame


def get_character_matrix(key):
    player_matrix = get_animation_matrix(key)
    for right_index in (1, 4):
        current_row = list(map(lambda cur: pygame.transform.flip(cur, True, False), player_matrix[right_index]))
        player_matrix.append(current_row)
    return player_matrix


def init_player(tmx_data):
    player_matrix = get_character_matrix("player_movement")
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


def init_enemy(name, health, damage, main_player, tmx_data):
    player_matrix = get_character_matrix("enemy_movement")
    player_matrix = [[pygame.transform.scale(c, (100, 100)) for c in row] for row in player_matrix]
    return Enemy(
        name,
        health,
        damage,
        player_matrix[0],
        player_matrix,
        tmx_data,
        main_player
    )
