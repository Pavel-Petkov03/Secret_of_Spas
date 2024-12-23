from player.display_mixins.display_movement_mixins.enemy_display_mixin import EnemyDisplayMixin
from player.display_mixins.animation_frame_requester import MoveAnimationFrameRequester, \
    InfantryAttackAnimationFrameRequester


class InfantryEnemyDisplayMixin(EnemyDisplayMixin):

    def __init__(self, *args, **kwargs):
        EnemyDisplayMixin.__init__(self, *args, **kwargs)
        self.stay_animation_frame_requester = MoveAnimationFrameRequester(
            self.get_animation_props()[self.direction]["stand_animation_frame"],
            50, 5, is_repeated=False
        )
        self.attack_animation_frame_requester = InfantryAttackAnimationFrameRequester(
            self.get_attack_props()[self.direction], 20, 5,
            is_repeated=False)

        self.stay_animation_frame_requester.next_animation_request = self.attack_animation_frame_requester
        self.attack_animation_frame_requester.next_animation_request = self.stay_animation_frame_requester
        self.current_direction = None
        self.is_in_range = False

    def update_state(self, screen, event_list, *args, **kwargs):
        if self.get_distance_to_player(screen) <= 1:
            if not self.is_in_range:
                self.main_animation_frame_requester = self.stay_animation_frame_requester
            if self.current_direction != self.direction:
                self.attack_animation_frame_requester.current_animation_frame = self.get_attack_props()[self.direction]
                self.stay_animation_frame_requester.current_animation_frame = self.get_animation_props()[self.direction]["stand_animation_frame"]
                self.current_direction = self.direction
            self.is_in_range = True
        else:
            self.main_animation_frame_requester = self.move_animation_frame_requester
            self.is_in_range = False
            super().update_state(screen, event_list, *args, **kwargs)

    def get_attack_props(self):
        return {
            "left": self.animation_frames[12],
            "right": self.animation_frames[7],
            "up": self.animation_frames[8],
            "down": self.animation_frames[6],
        }
