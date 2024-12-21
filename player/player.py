from errors import DeadError
from player.display_mixins.display_movement_mixins.infantry_enemy_display_mixin import InfantryEnemyDisplayMixin
from player.display_mixins.display_movement_mixins.player_display_mixin import PlayerDisplayMixin, \
    PlayerAttackDisplayMixin


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
        if value <= 0:
            raise DeadError("You are dead", self)
        self._health = value


class Player(Character, PlayerAttackDisplayMixin):
    def __init__(self, name, health, x, y, damage, current_animation_frame, animations_frames, dungeon_data):
        Character.__init__(self, name, health, damage)
        PlayerAttackDisplayMixin.__init__(self, x, y, current_animation_frame, animations_frames, dungeon_data)


class Enemy(Character, InfantryEnemyDisplayMixin):
    def __init__(self, name, health, damage, current_animation_frame, animation_frames, dungeon_data):
        Character.__init__(self, name, health, damage)
        InfantryEnemyDisplayMixin.__init__(self, current_animation_frame, animation_frames, dungeon_data)

    def attack(self):
        self.player.health -= self.damage
