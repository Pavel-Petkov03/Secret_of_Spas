from player.display_mixins.animation_frame_requester import MoveAnimationFrameRequester, \
    ArcherAttackAnimationFrameRequester
from player.display_mixins.display_movement_mixins.arrow_display_mixin import EnemyArrow
from player.display_mixins.display_movement_mixins.arrow_utils import init_arrow
from player.display_mixins.display_movement_mixins.enemy_display_mixin import EnemyDisplayMixin


class ArcherEnemyDisplayMixin(EnemyDisplayMixin):

    def __init__(self, *args, **kwargs):
        EnemyDisplayMixin.__init__(self, *args, **kwargs)
        self.stay_animation_frame_requester = ArcherAttackAnimationFrameRequester(
            self.get_animation_props()[self.direction]["stand_animation_frame"],
            50, 5, is_repeated=False, next_animation_request=self.move_animation_frame_requester
        )
        self.damage = None
        self.arrows = []
        self.current_direction = None
        self.is_in_range = False

    def update_state(self, screen, event_list, *args, **kwargs):
        if self.get_distance_to_player(screen) <= 4 and len(self.get_position_array()) == 1:
            if not isinstance(self.main_animation_frame_requester, ArcherAttackAnimationFrameRequester):
                self.main_animation_frame_requester = self.stay_animation_frame_requester
                self.arrows.append(init_arrow(1, self.dungeon_data, self, EnemyArrow))
        else:
            self.main_animation_frame_requester = self.move_animation_frame_requester
            super().update_state(screen, event_list, *args, **kwargs)
