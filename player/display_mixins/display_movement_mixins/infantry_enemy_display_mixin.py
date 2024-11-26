from player.display_mixins.display_movement_mixins.enemy_display_mixin import EnemyDisplayMixin
from player.display_mixins.animation_frame_requester import MoveAnimationFrameRequester, \
    InfantryAttackAnimationFrameRequester


class InfantryEnemyDisplayMixin(EnemyDisplayMixin):

    def __init__(self, *args, **kwargs):
        EnemyDisplayMixin.__init__(self, *args, **kwargs)
        self.stay_animation_frame_requester = MoveAnimationFrameRequester(
            self.get_animation_props()[self.direction]["stand_animation_frame"],
            20, 5, is_repeated=False
            )
        self.attack_animation_frame_requester = InfantryAttackAnimationFrameRequester(
            self.get_attack_props()[self.direction], 20, 5,
            is_repeated=False)

        self.stay_animation_frame_requester.next_animation_request = self.attack_animation_frame_requester
        self.attack_animation_frame_requester.next_animation_request = self.stay_animation_frame_requester
        self.current_direction = self.direction

    def update_state(self, screen):
        if self.get_distance_to_player(screen) <= 1:
            self.main_animation_frame_requester = self.attack_animation_frame_requester
        else:
            self.main_animation_frame_requester = self.move_animation_frame_requester
            super().update_state(screen)

    def get_attack_props(self):
        return {
            "left": self._animation_frames[12],
            "right": self._animation_frames[7],
            "up": self._animation_frames[8],
            "down": self._animation_frames[6],
        }
