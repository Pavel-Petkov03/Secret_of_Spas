import settings
from player.display_mixins.display_movement_mixins.arrow_display_mixin import PlayerArrow
from player.player import Player, EnemyArcher, EnemyInfantry
import player.settings as player_settings
from spritesheet.utils import get_animation_matrix
import pygame


def get_character_matrix(key):
    player_matrix = get_animation_matrix(key)
    for right_index in (1, 4, 7):
        current_row = list(map(lambda cur: pygame.transform.flip(cur, True, False), player_matrix[right_index]))
        player_matrix.append(current_row)
    return player_matrix


def init_player(dungeon_data):
    player_matrix = get_character_matrix("player_movement")
    return Player(
        player_settings.MAIN_PLAYER_NAME,
        player_settings.MAIN_PLAYER_HEALTH_POINTS,
        player_settings.MAIN_PLAYER_X_POS,
        player_settings.MAIN_PLAYER_Y_POS,
        player_settings.MAIN_PLAYER_DAMAGE_POINTS,
        player_matrix[0],
        player_matrix,
        dungeon_data
    )


def enemy_factory(name, health, damage, dungeon_data, is_infantry):
    player_matrix = get_character_matrix("enemy_movement")
    create_class = EnemyInfantry if is_infantry else EnemyArcher
    return create_class(
        name,
        health,
        damage,
        player_matrix[0],
        player_matrix,
        dungeon_data
    )



