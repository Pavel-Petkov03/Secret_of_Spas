import math
import random
from collections import deque
from abc import ABC, abstractmethod
import pygame

import settings


class DeadError(Exception):
    pass


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

    def update_state(self, screen):
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
        current_x = screen.get_width() / 2 / settings.SCALE_FACTOR / settings.TILE_WIDTH
        current_y = screen.get_height() / 2 / settings.SCALE_FACTOR / settings.TILE_HEIGHT
        player_map_x = int(current_x + new_x / settings.TILE_WIDTH)
        player_map_y = int(current_y + new_y / settings.TILE_HEIGHT)
        return self.collides_with_block(player_map_x, player_map_y)

    def get_map_tiled_position(self, screen):
        return tuple(map(int, self.get_map_position(screen)))


class PlayerDisplayMixin(CharacterDisplayMixin):

    def _trigger_update(self, screen):
        return True

    def update_state(self, screen):
        super().update_state(screen)
        self.move_to_x_y_plane(screen)

    def blit(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        new_x = (width / 2 + width / 2 - self.current_animation.get_width()) / 2
        new_y = (height / 2 - self.current_animation.get_height() + height / 2) / 2
        screen.blit(self.current_animation, (new_x, new_y))

    def get_map_position(self, screen):
        player_map_x = (self.x + screen.get_width() / 2) / settings.SCALE_FACTOR / settings.TILE_WIDTH
        player_map_y = (self.y + screen.get_height() / 2) / settings.SCALE_FACTOR / settings.TILE_HEIGHT
        return player_map_x, player_map_y

    def move_to_x_y_plane(self, screen):
        animation_props = self.get_animation_props()
        directions = ["left", "right", "up", "down"]
        for direction in directions:
            if self.trig_movement_in_direction(screen, direction, animation_props):
                break
        else:
            if animation_props.get(self.direction):
                self.current_animation_frame = animation_props[self.direction]["stand_animation_frame"]
            self.direction = "stand_" + self.direction

    def trig_movement_in_direction(self, screen, direction, animation_props):
        if self.is_triggered_movement(screen,
                                      *animation_props[direction]["moved_pos"],
                                      self.get_needed_press_keys_props()[direction]
                                      ):
            self.change_direction(direction)
            self.x, self.y = animation_props[direction]["moved_pos"]
            return True
        return False

    @staticmethod
    def get_needed_press_keys_props():
        keys = pygame.key.get_pressed()
        return {
            "left": (keys[pygame.K_LEFT], keys[pygame.K_a]),
            "right": (keys[pygame.K_RIGHT], keys[pygame.K_d]),
            "up": (keys[pygame.K_UP], keys[pygame.K_w]),
            "down": (keys[pygame.K_DOWN], keys[pygame.K_s])
        }


class EnemyDisplayMixin(CharacterDisplayMixin):

    def __init__(self, current_animation_frame, animations_frames, tmx_data, main_player):
        self.tmx_data = tmx_data
        x, y = self.get_random_pos()
        super().__init__(200, 300, current_animation_frame, animations_frames, tmx_data)
        self.main_player = main_player
        self.main_player_pos = None
        self.path_to_player = deque()

    def get_map_position(self, screen):
        map_x = (self.x + screen.get_width() / 2) / settings.SCALE_FACTOR / settings.TILE_WIDTH
        map_y = (self.y + screen.get_height() / 2) / settings.SCALE_FACTOR / settings.TILE_HEIGHT
        return map_x, map_y

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
        m_x, m_y = (self.x - self.main_player.x) * settings.SCALE_FACTOR, (self.y - self.main_player.y) * settings.SCALE_FACTOR
        cur_x, cur_y = screen.get_width() / 2, screen.get_height() / 2
        dx = m_x - cur_x
        dy = m_y - cur_y
        distance = math.sqrt(dx ** 2 + dy ** 2) // settings.TILE_WIDTH // settings.SCALE_FACTOR
        return int(distance) < 10

    def update_state(self, screen):
        current_pos = self.get_map_tiled_position(screen)
        b = self.main_player.get_map_tiled_position(screen)
        pygame.draw.line(screen, "black", (current_pos[0] * settings.TILE_WIDTH * settings.SCALE_FACTOR,
                                           current_pos[1] * settings.TILE_WIDTH * settings.SCALE_FACTOR),
                         (b[0] * settings.TILE_WIDTH * settings.SCALE_FACTOR,
                          b[1] * settings.TILE_WIDTH * settings.SCALE_FACTOR)
                         )
        super().update_state(screen)
        self.track_main_player(screen, current_pos)
        self.move_to_x_y_plane(screen)

    def track_main_player(self, screen, current_pos):
        current_main_player_pos = self.main_player.get_map_tiled_position(screen)
        if current_main_player_pos != self.main_player_pos:
            if self.main_player_pos:
                self.path_to_player.append(current_main_player_pos)
            else:

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
                print(self.path_to_player)
                return True
            visited.add(node)
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        return False

    def in_bounds(self, pos):
        return 0 <= pos[0] < settings.VIEW_PORT_TILES_W and 0 <= pos[1] <= settings.VIEW_PORT_TILES_H

    def get_neighbors(self, current):
        x, y = current
        appropriate_neighbors = [
            (x - 1, y),
            (x + 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        appropriate_neighbors = [pos for pos in appropriate_neighbors if self.in_bounds(pos) and not self.collides_with_block(*pos)]
        return appropriate_neighbors

    def move_to_x_y_plane(self, screen):
        if self.path_to_player:
            current_block = self.path_to_player[0]
            if current_block != self.get_map_tiled_position(screen):
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
        if self.main_player.x - settings.TILE_WIDTH <= self.x <= self.main_player.x + settings.VIEW_PORT_TILES_W * settings.TILE_WIDTH + settings.TILE_WIDTH \
                and self.main_player.y - settings.TILE_WIDTH <= self.y <= self.main_player.y + settings.VIEW_PORT_TILES_H * settings.TILE_HEIGHT + settings.TILE_WIDTH:
            screen.blit(self.current_animation, ((self.x - self.main_player.x) * settings.SCALE_FACTOR,
                                                 (self.y - self.main_player.y) * settings.SCALE_FACTOR))


class Character:
    def __init__(self, name, health, damage):
        self.name = name
        self._health = health
        self.damage = damage

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if self.health - value <= 0:
            raise DeadError("You are dead")
        self._health -= value


class Player(Character, PlayerDisplayMixin):
    def __init__(self, name, health, x, y, damage, current_animation_frame, animations_frames, tmx_data):
        Character.__init__(self, name, health, damage)
        PlayerDisplayMixin.__init__(self, x, y, current_animation_frame, animations_frames, tmx_data)


class Enemy(Character, EnemyDisplayMixin):
    def __init__(self, name, health, damage, current_animation_frame, animation_frames, tmx_data, main_player):
        Character.__init__(self, name, health, damage)
        EnemyDisplayMixin.__init__(self, current_animation_frame, animation_frames, tmx_data, main_player)

    def attack(self):
        self.main_player.health -= self.damage
