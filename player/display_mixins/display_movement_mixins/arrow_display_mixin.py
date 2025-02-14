import math
from abc import ABC, abstractmethod

import pygame

import settings
from errors import DeadError
from events.event_types.dungeos import REDIRECT_TO_ANOTHER_MAP
from events.item_drop_event import ItemDropEvent
from events.redirect_event import RedirectEvent
from player.display_mixins.animation_frame_requester import ArrowAttackAnimationFrameRequester, \
    DieEnemyAnimationFrameRequester
from player.display_mixins.display_movement_mixins.base_display_character_mixin import DisplayMixin


class ArrowDisplayMixin(DisplayMixin, ABC):
    def __init__(self, direction, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = direction
        self.main_animation_frame_requester = ArrowAttackAnimationFrameRequester(self.current_animation_frame, 20, 5,
                                                                                 is_repeated=True)
        self.player = self.dungeon_data.player
        self.mem_x = self.x
        self.mem_y = self.y
        self.damage = None
        self.movement_speed = 15
        self.executor = None

    def _trigger_update(self, screen):
        return True

    def clear_arrow(self):
        pass

    def update_state(self, screen, delta_time, event_list, *args, **kwargs):
        target_attacked = self.target_touched(screen)
        if target_attacked:
            self.decrease_damage_to_target(target_attacked, screen)
            self.executor.arrows.remove(self)
            target_attacked.get_map_position(screen)
        elif self.arrow_out_of_range() or self.collides_with_block(*self.get_map_position(screen)):
            self.executor.arrows.remove(self)
        else:
            self.move_arrow_on_x_y_plane()

    def decrease_damage_to_target(self, target, screen):
        pass

    @abstractmethod
    def target_touched(self, screen):
        pass

    def arrow_out_of_range(self):
        return max(abs(self.x - self.mem_x),
                   abs(self.y - self.mem_y)) / settings.TILE_WIDTH / settings.SCALE_FACTOR >= 15

    def move_arrow_on_x_y_plane(self):
        change_dir = {
            "left": (self.x - self.movement_speed, self.y),
            "right": (self.x + self.movement_speed, self.y),
            "up": (self.x, self.y - self.movement_speed),
            "down": (self.x, self.y + self.movement_speed),
            "stand_left": (self.x - self.movement_speed, self.y),
            "stand_right": (self.x + self.movement_speed, self.y),
            "stand_up": (self.x, self.y - self.movement_speed),
            "stand_down": (self.x, self.y + self.movement_speed),
        }
        self.x, self.y = change_dir[self.direction]


class PlayerArrowDisplayMixin(ArrowDisplayMixin):

    def clear_arrow(self):
        self.dungeon_data.player.arrows.remove(self)

    def target_touched(self, screen):
        current_pos = self.get_map_position(screen)
        for enemy in self.dungeon_data.enemies:
            if current_pos == enemy.get_map_position(screen):
                return enemy

    def decrease_damage_to_target(self, target, screen):
        try:
            target.health -= self.damage
        except DeadError:
            if not isinstance(target.main_animation_frame_requester, DieEnemyAnimationFrameRequester):
                target.main_animation_frame_requester = DieEnemyAnimationFrameRequester(
                    target.animation_frames[9],
                    20,
                    5,
                    is_repeated=False,
                    to_remove=target
                )
                self.play_dead_sound()
                current_event = ItemDropEvent(dungeon_state=self.dungeon_data, additional_state={
                    "x": target.x,
                    "y": target.y
                })
                current_event.start()

    @staticmethod
    def play_dead_sound():
        hit_sound = pygame.mixer.Sound("audio/dead.ogg")
        hit_sound.play()

    def get_map_position(self, screen):
        current_x = screen.get_width() / 2 / settings.SCALE_FACTOR / settings.TILE_WIDTH
        current_y = screen.get_height() / 2 / settings.SCALE_FACTOR / settings.TILE_HEIGHT
        player_map_x = int(current_x + self.x / settings.TILE_WIDTH)
        player_map_y = int(current_y + self.y / settings.TILE_HEIGHT)
        return player_map_x, player_map_y

    def blit(self, screen):
        screen_x = (self.x - self.dungeon_data.player.x) * settings.SCALE_FACTOR + settings.SCREEN_WIDTH / 2
        screen_y = (self.y - self.dungeon_data.player.y) * settings.SCALE_FACTOR + settings.SCREEN_HEIGHT / 2
        screen_x = (2 * screen_x - self.main_animation_frame_requester.current_animation.get_width()) / 2
        screen_y = (2 * screen_y - self.main_animation_frame_requester.current_animation.get_height()) / 2
        screen.blit(self.main_animation_frame_requester.current_animation, (screen_x, screen_y))


class EnemyArrowDisplayMixin(ArrowDisplayMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def target_touched(self, screen):
        if self.get_map_position(screen) == self.dungeon_data.player.get_map_position(screen):
            return self.dungeon_data.player

    def get_map_position(self, screen):
        screen_x = self.x // settings.TILE_WIDTH
        screen_y = self.y // settings.TILE_HEIGHT
        return screen_x, screen_y

    def decrease_damage_to_target(self, target, screen):
        try:
            target.health -= self.damage
        except DeadError:
            current_event = RedirectEvent(REDIRECT_TO_ANOTHER_MAP, additional_state={
                "redirect_url": "village"
            })
            current_event.start()


class PlayerArrow(PlayerArrowDisplayMixin):
    def __init__(self, executor, damage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = executor
        self.damage = damage
        self.player = self.dungeon_data.player


class EnemyArrow(EnemyArrowDisplayMixin):
    def __init__(self, executor, damage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage = damage
        self.executor = executor
        self.movement_speed = 5
