from player.player import Player
import player.settings as settings


def init_player(tmx_data):
    return Player(
        settings.MAIN_PLAYER_NAME,
        settings.MAIN_PLAYER_HEALTH_POINTS,
        settings.MAIN_PLAYER_X_POS,
        settings.MAIN_PLAYER_Y_POS,
        settings.MAIN_PLAYER_DAMAGE_POINTS,
        settings.MAIN_PLAYER_CURRENT_ANIMATION_FRAME,
        settings.MAIN_PLAYER_ANIMATION_FRAMES,
        tmx_data
    )
