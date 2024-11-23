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


class PlayerDisplayMixin(CharacterDisplayMixin):
    def _trigger_update(self, screen):
        return True

    def update_state(self, screen):
        super().update_state(screen)
        keys = pygame.key.get_pressed()
        if self.is_triggered_movement(screen, (keys[pygame.K_LEFT], keys[pygame.K_a]), self.x - self.movement_speed,
                                      self.y):
            self.change_direction("left", self._animation_frames[11])
            self.x -= self.movement_speed
        elif self.is_triggered_movement(screen, (keys[pygame.K_RIGHT], keys[pygame.K_d]), self.x + self.movement_speed,
                                        self.y):
            self.change_direction("right", self._animation_frames[4])
            self.x += self.movement_speed
        elif self.is_triggered_movement(screen, (keys[pygame.K_UP], keys[pygame.K_w]), self.x,
                                        self.y - self.movement_speed):
            self.change_direction("up", self._animation_frames[5])
            self.y -= self.movement_speed
        elif self.is_triggered_movement(screen, (keys[pygame.K_DOWN], keys[pygame.K_s]), self.x,
                                        self.y + self.movement_speed):
            self.change_direction("down", self._animation_frames[3])
            self.y += self.movement_speed
        else:
            if self.direction == "down":
                self.current_animation_frame = self._animation_frames[0]
            elif self.direction == "right":
                self.current_animation_frame = self._animation_frames[1]
            elif self.direction == "up":
                self.current_animation_frame = self._animation_frames[2]
            elif self.direction == "left":
                self.current_animation_frame = self._animation_frames[10]
            self.direction = "stand_" + self.direction

    def change_direction(self, direction, new_animation_frame):
        if not self.direction == direction:
            self.current_animation_frame = new_animation_frame
        self.direction = direction

    def is_triggered_movement(self, screen, keys_list, new_x, new_y):
        return any(keys_list) and not self.move_to_block(screen, new_x, new_y)

    def blit(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        new_x = (width / 2 + width / 2 - self.current_animation.get_width()) / 2
        new_y = (height / 2 - self.current_animation.get_height() + height / 2) / 2
        screen.blit(self.current_animation, (new_x, new_y))

    def move_to_block(self, screen, new_x, new_y):
        current_x, current_y = self.get_map_position(screen)
        player_map_x = int(current_x + new_x / settings.TILE_WIDTH)
        player_map_y = int(current_y + new_y / settings.TILE_HEIGHT)
        return self.collides_with_block(player_map_x, player_map_y)

    def get_map_position(self, screen):
        player_map_x = screen.get_width() / 2 / settings.SCALE_FACTOR / settings.TILE_WIDTH
        player_map_y = screen.get_width() / 2 / settings.SCALE_FACTOR / settings.TILE_HEIGHT
        return player_map_x, player_map_y


class EnemyDisplayMixin(CharacterDisplayMixin):
    def __init__(self, current_animation_frame, animations_frames, tmx_data, main_player):
        self.tmx_data = tmx_data
        x, y = self.get_random_pos()
        super().__init__(x, y, current_animation_frame, animations_frames, tmx_data)
        self.main_player = main_player
        self.main_player_pos = None
        self.path_to_player = []

    def get_map_position(self, screen):
        map_x = self.x / settings.SCALE_FACTOR / settings.TILE_WIDTH
        map_y = self.y / settings.SCALE_FACTOR / settings.TILE_HEIGHT
        return map_x, map_y

    def get_random_pos(self):
        while True:
            x = random.randint(0, settings.MAP_WIDTH)
            y = random.randint(0, settings.MAP_HEIGHT)
            if self.collides_with_block(x, y):
                continue
            return x, y

    def _trigger_update(self, screen):
        m_x, m_y = self.main_player.get_map_position(screen)
        cur_x, cur_y = self.get_map_position(screen)
        dx = m_x - cur_x
        dy = m_y - cur_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return int(distance) < 20

    def update_state(self, screen):
        super().update_state(screen)
        current_main_player_pos = self.main_player.get_map_position(screen)
        if current_main_player_pos != self.main_player_pos:
            if self.main_player_pos:
                self.path_to_player.append(current_main_player_pos)
            else:
                current = self.get_map_position(screen)
                self.get_main_player_trail(current, self.main_player_pos, self.path_to_player, set())


    def get_main_player_trail(self, current, target, path, visited):
        if current == target:
            path.append(current)
            return True
        visited.add(current)
        for neighbor in self.get_neighbors(current):
            if neighbor not in visited:
                if self.get_main_player_trail(neighbor, target, path, visited):
                    path.append(current)
                    return True
        return False

    def get_neighbors(self, current):
        x, y = current
        appropriate_neighbors = [
            (x - 1, y),
            (x + 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        appropriate_neighbors = [pos for pos in appropriate_neighbors if not self.collides_with_block(*pos)]
        return appropriate_neighbors


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
