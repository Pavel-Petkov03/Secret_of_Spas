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
        new_x = (settings.SCREEN_WIDTH / 2 + settings.SCREEN_WIDTH / 2 - self.current_animation.get_width()) / 2
        new_y = (settings.SCREEN_HEIGHT / 2 - self.current_animation.get_height() + settings.SCREEN_HEIGHT / 2) / 2
        screen.blit(self.current_animation, (new_x, new_y))


    def move_to_block(self, screen, new_x, new_y):
        current_x, current_y = self.get_map_position(screen)
        player_map_x = int(current_x + new_x / settings.TILE_WIDTH)
        player_map_y = int(current_y + new_y / settings.TILE_HEIGHT)
        return self.collides_with_block(player_map_x, player_map_y)

    def get_map_position(self, screen):
        player_map_x = screen.get_width() / 2 / settings.SCALE_FACTOR / settings.TILE_WIDTH
        player_map_y = screen.get_height() / 2 / settings.SCALE_FACTOR / settings.TILE_HEIGHT
        return player_map_x, player_map_y


class EnemyDisplayMixin(CharacterDisplayMixin):
    pass


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
        CharacterDisplayMixin.__init__(self, x, y, current_animation_frame, animations_frames, tmx_data)


class Enemy(Character, EnemyDisplayMixin):
    def __init__(self, name, health, damage, current_animation_frame, animation_frames, tmx_data):
        Character.__init__(self, name, health, damage)
        self.tmx_data = tmx_data
        x, y = self.get_random_pos()
        CharacterDisplayMixin.__init__(self, x, y, current_animation_frame, animation_frames, tmx_data)

    def get_random_pos(self):
        while True:
            x = random.randint(0, settings.MAP_WIDTH)
            y = random.randint(0, settings.MAP_HEIGHT)
            if self.collides_with_block(x, y):
                continue
            return x, y
