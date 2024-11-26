import settings
from collections import deque
from abc import ABC, abstractmethod


class CharacterDisplayMixin(ABC):
    def __init__(self, x, y, current_animation_frame, animation_frames, tmx_data):
        self.x = x
        self.y = y
        self._current_animation_frame = deque(current_animation_frame)
        self._animation_frames = animation_frames
        self.direction = "down"
        self.tmx_data = tmx_data
        self.movement_speed = 0.7
        self.counter = 0

    def change_frame(self):
        self._current_animation_frame.append(self._current_animation_frame.popleft())

    @property
    def current_animation(self):
        return self._current_animation_frame[0]

    @property
    def current_animation_frame(self):
        return self._current_animation_frame

    @current_animation_frame.setter
    def current_animation_frame(self, value):
        self._current_animation_frame = deque(value)

    def update(self, screen):
        if self._trigger_update(screen):
            self.update_state(screen)
            self.iterate_over_frames()
        else:
            self.clear_update_state(screen)
            self.iterate_over_frames()

    def clear_update_state(self, screen):
        pass

    def update_state(self, screen):
        pass

    def iterate_over_frames(self):
        if self.counter == 5:
            self.change_frame()
            self.counter = 0
        self.counter += 1

    @abstractmethod
    def _trigger_update(self, screen):
        pass

    def blit(self, screen):
        pass

    @abstractmethod
    def get_map_position(self, screen):
        pass

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
                "stand_animation_frame": self._animation_frames[10],
                "animation_frame": self._animation_frames[11],
                "moved_pos": (self.x - self.movement_speed, self.y),

            },
            "right": {
                "stand_animation_frame": self._animation_frames[1],
                "animation_frame": self._animation_frames[4],
                "moved_pos": (self.x + self.movement_speed, self.y),
            }, "up": {
                "stand_animation_frame": self._animation_frames[2],
                "animation_frame": self._animation_frames[5],
                "moved_pos": (self.x, self.y - self.movement_speed)
            }, "down": {
                "stand_animation_frame": self._animation_frames[0],
                "animation_frame": self._animation_frames[3],
                "moved_pos": (self.x, self.y + self.movement_speed)
            }
        }

    def change_direction(self, direction):
        if direction != self.direction:
            self.current_animation_frame = self.get_animation_props()[direction]["animation_frame"]
        self.direction = direction

    def is_triggered_movement(self, screen, new_x, new_y, bool_requirements_list):
        return any(bool_requirements_list) and not self.move_to_block(screen, new_x, new_y)

    def move_to_block(self, screen, new_x, new_y):
        pass

    def get_map_tiled_position(self, screen):
        return tuple(map(int, self.get_map_position(screen)))
