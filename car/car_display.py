import pygame

import settings
from decorators.is_in_blit_range import IsInBlitRange
from player.display_mixins.display_movement_mixins.player_display_mixin import PlayerDisplayMixin


class CarDisplayMixin(PlayerDisplayMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_mount = False
        self.player = self.dungeon_data.player
        self.movement_speed = 8

    def get_map_position(self, screen):
        if self.is_mount:
            return super().get_map_position(screen)
        return self.unmount_map_position(screen)

    def blit(self, screen):
        if self.is_mount:
            return super().blit(screen)
        return self.unmount_blit(screen)

    def unmount_map_position(self, screen):
        tile_x = self.x // settings.TILE_WIDTH
        tile_y = self.y // settings.TILE_WIDTH
        return tile_x, tile_y

    def update(self, screen, delta_time, *args, **kwargs):
        if self.is_mount:
            super().update(screen, delta_time, *args, **kwargs)

    def unmount_blit(self, screen):
        self.__unmount_blit(self.x, self.y, screen, self.main_animation_frame_requester.current_animation)

    @IsInBlitRange
    def __unmount_blit(self, x, y, screen, image):
        screen_x = (x - self.dungeon_data.player.x) * settings.SCALE_FACTOR
        screen_y = (y - self.dungeon_data.player.y) * settings.SCALE_FACTOR
        screen_x = (2 * screen_x - image.get_width()) / 2
        screen_y = (2 * screen_y - image.get_height()) / 2
        screen.blit(image, (screen_x, screen_y))

    def get_animation_props(self):
        return {
            "left": {
                "animation_frame": self.animation_frames[0],
                "moved_pos": (self.x - self.movement_speed, self.y),
            },
            "up": {
                "animation_frame": self.animation_frames[1],
                "moved_pos": (self.x, self.y - self.movement_speed),

            },
            "right": {
                "animation_frame": self.animation_frames[2],
                "moved_pos": (self.x + self.movement_speed, self.y)
            },
            "down": {
                "animation_frame": self.animation_frames[3],
                "moved_pos": (self.x, self.y + self.movement_speed)
            }
        }

    def handle_stand_animation(self, animation_props, directions):
        pass


class Car(CarDisplayMixin):
    pass
