import math

import pygame.draw

from decorators.is_in_blit_range import IsInBlitRange
from errors import DeadError
from player.display_mixins.display_movement_mixins.base_display_character_mixin import CharacterDisplayMixin
import settings
from collections import deque
import random


class EnemyDisplayMixin(CharacterDisplayMixin):

    def __init__(self, current_animation_frame, animations_frames, dungeon_data):
        self.tmx_data = dungeon_data.tmx_data
        x, y = self.get_random_pos()
        super().__init__(x, y, current_animation_frame, animations_frames, dungeon_data)
        self.main_player_pos = None
        self.path_to_player = deque()
        self.no_path_to_player = False
        self.player = self.dungeon_data.player

    def get_map_position(self):
        x = int(self.x / settings.TILE_WIDTH)
        y = int(self.y / settings.TILE_HEIGHT)
        return x, y

    def move_to_block(self, screen, new_x, new_y):
        x = int(new_x / settings.TILE_WIDTH)
        y = int(new_y / settings.TILE_HEIGHT)
        return self.collides_with_block(x, y)

    def get_random_pos(self):
        while True:
            x = random.randint(0, settings.MAP_WIDTH - settings.TILE_WIDTH)
            y = random.randint(0, settings.MAP_HEIGHT - settings.TILE_HEIGHT)

            map_x = int(x / settings.TILE_WIDTH)
            map_y = int(y / settings.TILE_HEIGHT)

            if self.collides_with_block(map_x, map_y):
                continue
            return x, y

    def _trigger_update(self, screen):
        distance = self.get_distance_to_player()
        is_in_range = distance < 5
        if self.no_path_to_player:
            self.no_path_to_player = is_in_range
        return is_in_range and not self.no_path_to_player

    def get_distance_to_player(self):
        current_tile_x, current_tile_y = self.get_map_position()
        main_player_x, main_player_y = self.player.get_map_position()
        dx = current_tile_x - main_player_x
        dy = current_tile_y - main_player_y
        return math.sqrt(dx ** 2 + dy ** 2)

    def update_state(self, screen, event_list, *args, **kwargs):
        current_pos = self.get_map_position()
        self.track_main_player(screen, current_pos)
        self.move_to_x_y_plane(screen)

    def track_main_player(self, screen, current_pos):
        current_main_player_pos = self.player.get_map_position()
        if current_main_player_pos != self.main_player_pos:
            self.get_main_player_trail(current_pos, self.player.get_map_position())
            self.path_to_player = deque(self.path_to_player)
            if self.path_to_player:
                self.main_player_pos = self.path_to_player[-1]

    def get_main_player_trail(self, current, target):
        queue = deque([(current, [current])])
        visited = set()
        counter = 0
        while queue:
            node, path = queue.popleft()
            counter += 1
            if counter == 1000:
                self.no_path_to_player = True
                return False
            if node == target:
                self.path_to_player = path
                return True
            visited.add(node)
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        return False

    @staticmethod
    def in_bounds(pos):
        return 0 <= pos[0] < 100 and 0 <= pos[1] < 100

    def get_neighbors(self, current):
        x, y = current
        appropriate_neighbors = [
            (x - 1, y),
            (x + 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        appropriate_neighbors = [pos for pos in appropriate_neighbors if
                                 self.in_bounds(pos) and not self.collides_with_block(*pos)]
        return appropriate_neighbors

    def clear_update_state(self, screen):
        if self.get_animation_props().get(self.direction):
            self.main_animation_frame_requester.current_animation_frame = self.get_animation_props()[self.direction][
                "stand_animation_frame"]
        if self.direction in ("left", "right", "up", "down"):
            self.direction = "stand_" + self.direction

    def move_to_x_y_plane(self, screen):
        if self.path_to_player:
            current_block = self.path_to_player[0]
            if current_block != self.get_map_position():
                self.path_to_player.popleft()
                return
            for direction in self.get_position_array():
                if self.is_triggered_movement(screen, *self.get_animation_props()[direction]["moved_pos"], (True,)):
                    self.change_direction(direction)
                    self.x, self.y = self.get_animation_props()[direction]["moved_pos"]
                    return

    def get_position_array(self):
        current_block = self.path_to_player[0]
        res = []
        if self.main_player_pos[0] < current_block[0]:
            res.append("left")
        elif self.main_player_pos[0] > current_block[0]:
            res.append("right")
        if self.main_player_pos[1] < current_block[1]:
            res.append("up")
        elif self.main_player_pos[1] > current_block[1]:
            res.append("down")
        return res

    def blit(self, screen):
        self.__blit(self.x, self.y, screen, self.main_animation_frame_requester.current_animation)

    @IsInBlitRange
    def __blit(self, x, y, screen, image):
        screen_x = (x - self.player.x) * settings.SCALE_FACTOR
        screen_y = (y - self.player.y) * settings.SCALE_FACTOR
        screen_x = (2 * screen_x - image.get_width()) / 2
        screen_y = (2 * screen_y - image.get_height()) / 2
        screen.blit(image, (screen_x, screen_y))

    def update(self, screen, delta_time, *args, **kwargs):
        try:
            super().update(screen, delta_time, *args, **kwargs)
        except DeadError as error:
            error.character.die()
