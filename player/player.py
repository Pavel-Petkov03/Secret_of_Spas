from player.display_mixins.display_movement_mixins.enemy_display_mixin import EnemyDisplayMixin
from player.display_mixins.display_movement_mixins.infantry_enemy_display_mixin import InfantryEnemyDisplayMixin
from player.display_mixins.display_movement_mixins.player_display_mixin import PlayerDisplayMixin


class DeadError(Exception):
    pass


class Character:
    def __init__(self, name, health, damage):
        self.name = name
        self._health = health
        self.damage = damage

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if self.health - value <= 0:
            raise DeadError("You are dead")
        self._health -= value


class Player(Character, PlayerDisplayMixin):
    def __init__(self, name, health, x, y, damage, current_animation_frame, animations_frames, tmx_data):
        Character.__init__(self, name, health, damage)
        PlayerDisplayMixin.__init__(self, x, y, current_animation_frame, animations_frames, tmx_data)


class Enemy(Character, InfantryEnemyDisplayMixin):
    def __init__(self, name, health, damage, current_animation_frame, animation_frames, tmx_data, main_player):
        Character.__init__(self, name, health, damage)
        InfantryEnemyDisplayMixin.__init__(self, current_animation_frame, animation_frames, tmx_data, main_player)

    def attack(self):
        self.main_player.health -= self.damage
