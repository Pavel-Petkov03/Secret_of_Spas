import math

from player.display_mixins.display_movement_mixins.base_display_character_mixin import CharacterDisplayMixin
import pygame
import settings
from collections import deque
import random


class EnemyDisplayMixin(CharacterDisplayMixin):

    def __init__(self, current_animation_frame, animations_frames, tmx_data, main_player):
        self.tmx_data = tmx_data
        x, y = self.get_random_pos()
        super().__init__(700, 500, current_animation_frame, animations_frames, tmx_data)
        self.main_player = main_player
        self.main_player_pos = None
        self.path_to_player = deque()
        self.player_is_target = False

    def get_map_position(self, screen):
        x = int(self.x / settings.TILE_WIDTH)
        y = int(self.y / settings.TILE_HEIGHT)
        screen_x = (x * settings.TILE_WIDTH - self.main_player.x) * settings.SCALE_FACTOR
        screen_y = (y * settings.TILE_HEIGHT - self.main_player.y) * settings.SCALE_FACTOR
        pygame.draw.rect(screen, (200, 200, 200),
                         (
                             screen_x,
                             screen_y
                             , settings.TILE_WIDTH * settings.SCALE_FACTOR,
                             settings.TILE_WIDTH * settings.SCALE_FACTOR
                         )
                         )
        return int(x), int(y)

    def get_random_pos(self):
        while True:
            x = random.randint(0, settings.MAP_WIDTH)
            y = random.randint(0, settings.MAP_HEIGHT)

            map_x = int(x / settings.SCALE_FACTOR / settings.TILE_WIDTH)
            map_y = int(y / settings.SCALE_FACTOR / settings.TILE_HEIGHT)

            if self.collides_with_block(map_x, map_y):
                continue
            return x, y

    def _trigger_update(self, screen):
        m_x, m_y = (self.x - self.main_player.x) * settings.SCALE_FACTOR, (
                self.y - self.main_player.y) * settings.SCALE_FACTOR
        cur_x, cur_y = screen.get_width() / 2, screen.get_height() / 2
        dx = m_x - cur_x
        dy = m_y - cur_y
        distance = math.sqrt(dx ** 2 + dy ** 2) // settings.TILE_WIDTH
        print(self.get_map_position(screen))
        print(self.main_player.get_map_position(screen))
        return int(distance) < 0

    def update_state(self, screen):
        current_pos = self.get_map_tiled_position(screen)
        super().update_state(screen)
        self.track_main_player(screen, current_pos)
        self.move_to_x_y_plane(screen)

    def track_main_player(self, screen, current_pos):
        current_main_player_pos = self.main_player.get_map_tiled_position(screen)
        if current_main_player_pos != self.main_player_pos:
            self.get_main_player_trail(current_pos, self.main_player.get_map_tiled_position(screen))
            self.path_to_player = deque(self.path_to_player)
            self.main_player_pos = self.path_to_player[-1]

    def get_main_player_trail(self, current, target):
        queue = deque([(current, [current])])
        visited = set()
        while queue:
            node, path = queue.popleft()
            if node == target:
                self.path_to_player = path
                return True
            visited.add(node)
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        return False

    def in_bounds(self, pos):
        return 0 <= pos[0] <= 32 and 0 <= pos[1] <= 32

    def get_neighbors(self, current):
        x, y = current
        appropriate_neighbors = [
            (x - 1, y),
            (x + 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        appropriate_neighbors = [pos for pos in appropriate_neighbors if self.in_bounds(pos)]
        return appropriate_neighbors

    def clear_update_state(self, screen):
        pass

    def move_to_x_y_plane(self, screen):
        if self.path_to_player:
            current_block = self.path_to_player[0]
            if current_block != self.get_map_tiled_position(screen) or current_block == self.main_player:
                self.path_to_player.popleft()
                return
            target_block = self.main_player_pos
            res = []
            if target_block[0] < current_block[0]:
                res.append("left")
            elif target_block[0] < current_block[0]:
                res.append("right")
            if target_block[1] < current_block[1]:
                res.append("up")
            elif target_block[1] > current_block[1]:
                res.append("down")
            for direction in res:
                if self.is_triggered_movement(screen, *self.get_animation_props()[direction]["moved_pos"], (True,)):
                    self.change_direction(direction)
                    self.x, self.y = self.get_animation_props()[direction]["moved_pos"]
                    return

    def blit(self, screen):
        if self.main_player.x <= self.x <= self.main_player.x + settings.VIEW_PORT_TILES_W * settings.TILE_WIDTH \
                and self.main_player.y <= self.y <= self.main_player.y + settings.VIEW_PORT_TILES_H * settings.TILE_HEIGHT:
            screen_x = (self.x - self.main_player.x) * settings.SCALE_FACTOR
            screen_y = (self.y - self.main_player.y) * settings.SCALE_FACTOR
            screen_x = (2 * screen_x - self.current_animation.get_width()) / 2
            screen_y = (2 * screen_y - self.current_animation.get_height()) / 2
            screen.blit(self.current_animation, (screen_x, screen_y))
