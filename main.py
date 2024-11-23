import math
from collections import deque

import pygame
from pytmx.util_pygame import load_pygame
import settings
from player.utils import init_player


class Game:
    def __init__(self):
        self.screen = settings.SCREEN
        self.scale_factor = math.ceil(settings.CURRENT_MAX_DIMENSION / settings.TILE_WIDTH / settings.VIEW_PORT_TILES_W)
        self.tmx_data = load_pygame("src/tiles/level_1.tmx")
        self.scale_grid()

        self.movement_speed = 0.7
        self.clock = pygame.time.Clock()
        self.counter = 0
        self.direction = None
        self.player = init_player()
        self.movement_speed = 0.7
        self.current_start_pos_x = 750
        self.current_start_pos_y = 100

    def scale_grid(self):
        for gid, image in enumerate(self.tmx_data.images):
            if image is not None:
                new_width = image.get_width() * self.scale_factor
                new_height = image.get_height() * self.scale_factor
                scaled_image = pygame.transform.scale(image, (new_width, new_height))
                self.tmx_data.images[gid] = scaled_image

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(60)

    def move_player(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not self.collide_with_block(
                self.current_start_pos_x - self.movement_speed,
                self.current_start_pos_y):
            if not self.direction == "left":
                self.player.current_animation_frame = deque(self.player.animation_frames[11])
            self.current_start_pos_x -= self.movement_speed
            self.direction = "left"
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not self.collide_with_block(
                self.current_start_pos_x + self.movement_speed,
                self.current_start_pos_y):
            if not self.direction == "right":
                self.player.current_animation_frame = deque(self.player.animation_frames[4])
            self.direction = "right"
            self.current_start_pos_x += self.movement_speed
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and not self.collide_with_block(self.current_start_pos_x,
                                                                                   self.current_start_pos_y - self.movement_speed):
            if not self.direction == "up":
                self.player.current_animation_frame = deque(self.player.animation_frames[5])
            self.direction = "up"
            self.current_start_pos_y -= self.movement_speed
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not self.collide_with_block(self.current_start_pos_x,
                                                                                     self.current_start_pos_y + self.movement_speed):
            if not self.direction == "down":
                self.player.current_animation_frame = deque(self.player.animation_frames[3])
            self.current_start_pos_y += self.movement_speed
            self.direction = "down"

    def collide_with_block(self, new_x, new_y):
        player_map_x = int((self.screen.get_width() / 2 / self.scale_factor + new_x) // settings.TILE_WIDTH)
        player_map_y = int((self.screen.get_height() / 2 / self.scale_factor + new_y) // settings.TILE_HEIGHT)

        result = self.get_tile_properties(player_map_x, player_map_y, self.tmx_data.layers[-1])
        return result and result["is_block"]

    def render_map(self):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, tile in layer.tiles():
                    if self.current_start_pos_x - settings.TILE_WIDTH <= x * settings.TILE_WIDTH <= self.current_start_pos_x + settings.VIEW_PORT_TILES_W * settings.TILE_WIDTH + settings.TILE_WIDTH \
                            and self.current_start_pos_y - settings.TILE_WIDTH <= y * settings.TILE_HEIGHT <= self.current_start_pos_y + settings.VIEW_PORT_TILES_H * settings.TILE_HEIGHT + settings.TILE_WIDTH:
                        screen_x = (x * settings.TILE_WIDTH - self.current_start_pos_x) * self.scale_factor
                        screen_y = (y * settings.TILE_HEIGHT - self.current_start_pos_y) * self.scale_factor
                        self.screen.blit(tile, (screen_x, screen_y))

    def update(self):
        self.move_player()
        self.render_map()
        image = self.player.get_current_animation_image()
        if self.counter == 5:
            self.player.rotate()
            self.counter = 0
        self.counter += 1
        new_x = (self.screen.get_width() / 2 + self.screen.get_width() / 2 - image.get_width()) / 2
        new_y = (self.screen.get_height() / 2 - image.get_height() + self.screen.get_height() / 2) / 2
        self.screen.blit(image, (new_x, new_y))

    def get_tile_properties(self, x, y, layer):
        if layer and hasattr(layer, 'tiles'):
            gid = layer.data[y][x]
            properties = self.tmx_data.get_tile_properties_by_gid(gid)
            return properties
        return None


if __name__ == "__main__":
    game = Game()
    game.run()
