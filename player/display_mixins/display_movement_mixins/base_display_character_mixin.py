from collections import deque
from abc import ABC, abstractmethod

import settings
from decorators.is_in_blit_range import IsInBlitRange
from player.display_mixins.animation_frame_requester import AnimationFrameDoneError, MoveAnimationFrameRequester, \
    DieEnemyAnimationFrameRequester


class DisplayMixin(ABC):
    def __init__(self, x, y, current_animation_frame, animation_frames, dungeon_data):
        self.x = x
        self.y = y
        self.current_animation_frame = deque(current_animation_frame)
        self.animation_frames = animation_frames
        self.dungeon_data = dungeon_data
        self.main_animation_frame_requester = None
        self.direction = None

    def update(self, screen, delta_time, *args, **kwargs):
        try:
            if self._trigger_update(screen):
                self.update_state(screen, delta_time, *args, **kwargs)
                self.main_animation_frame_requester.run(screen, self.__dict__, delta_time)
            else:
                self.clear_update_state(screen)
                self.main_animation_frame_requester.run(screen, self.__dict__, delta_time)
        except AnimationFrameDoneError as error:
            self.main_animation_frame_requester = error.next_animation_frame

    def clear_update_state(self, screen):
        pass

    def _trigger_update(self, screen):
        pass

    def update_state(self, screen, delta_time, event_list, *args, **kwargs):
        pass

    def blit(self, screen):
        self.__blit(self.x, self.y, screen, self.main_animation_frame_requester.current_animation)

    @IsInBlitRange
    def __blit(self, x, y, screen, image):
        screen_x = (x - self.dungeon_data.player.x) * settings.SCALE_FACTOR
        screen_y = (y - self.dungeon_data.player.y) * settings.SCALE_FACTOR
        screen_x = (2 * screen_x - image.get_width()) / 2
        screen_y = (2 * screen_y - image.get_height()) / 2
        screen.blit(image, (screen_x, screen_y))

    def get_map_position(self):
        tile_x = self.x // settings.TILE_WIDTH
        tile_y = self.y // settings.TILE_WIDTH
        return tile_x, tile_y


class CharacterDisplayMixin(DisplayMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tmx_data = self.dungeon_data.tmx_data
        self.direction = "down"
        self.move_animation_frame_requester = MoveAnimationFrameRequester(self.current_animation_frame, 20, 5)
        self.main_animation_frame_requester = self.move_animation_frame_requester
        self.movement_speed = 2

    def get_tile_properties(self, x, y, layer):
        if layer and hasattr(layer, 'tiles'):
            gid = layer.data[y][x]
            properties = self.tmx_data.get_tile_properties_by_gid(gid)
            return properties
        return None

    def collides_with_block(self, x, y):
        for layer in self.tmx_data.layers:
            result = self.get_tile_properties(x, y, layer)
            if result and result["is_block"]:
                return True
        return False

    def move_to_x_y_plane(self, screen):
        pass

    def get_animation_props(self):
        return {
            "left": {
                "stand_animation_frame": self.animation_frames[10],
                "animation_frame": self.animation_frames[11],
                "moved_pos": (self.x - self.movement_speed, self.y),
            },
            "right": {
                "stand_animation_frame": self.animation_frames[1],
                "animation_frame": self.animation_frames[4],
                "moved_pos": (self.x + self.movement_speed, self.y),
            }, "up": {
                "stand_animation_frame": self.animation_frames[2],
                "animation_frame": self.animation_frames[5],
                "moved_pos": (self.x, self.y - self.movement_speed)
            }, "down": {
                "stand_animation_frame": self.animation_frames[0],
                "animation_frame": self.animation_frames[3],
                "moved_pos": (self.x, self.y + self.movement_speed)
            }
        }

    def change_direction(self, direction):
        if direction != self.direction:
            self.main_animation_frame_requester.current_animation_frame = self.get_animation_props()[direction][
                "animation_frame"]
        self.direction = direction

    def is_triggered_movement(self, screen, new_x, new_y, bool_requirements_list):
        return any(bool_requirements_list) and not self.move_to_block(screen, new_x, new_y)

    def move_to_block(self, screen, new_x, new_y):
        pass
