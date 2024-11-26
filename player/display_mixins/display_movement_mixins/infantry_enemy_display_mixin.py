from player.display_mixins.display_movement_mixins.enemy_display_mixin import EnemyDisplayMixin


class InfantryEnemyDisplayMixin(EnemyDisplayMixin):

    def __init__(self, *args, **kwargs):
        EnemyDisplayMixin.__init__(self, *args, **kwargs)
        self.attack_awaiting_frames = 120
        self.another_counter = 0

    def update_state(self, screen):
        if self.get_distance_to_player(screen) <= 1:
            if self.another_counter == self.attack_awaiting_frames:
                self.current_animation_frame = self.get_attack_props()[self.direction]
                self.another_counter = 0
        else:
            super().update_state(screen)

    def get_attack_props(self):
        return {
            "left": self._animation_frames[12],
            "right": self._animation_frames[7],
            "up": self._animation_frames[8],
            "down": self._animation_frames[6],
        }
