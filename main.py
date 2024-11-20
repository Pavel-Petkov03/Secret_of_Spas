import math
import pygame
from pytmx.util_pygame import load_pygame
from settings import TILE_WIDTH, TILE_HEIGHT, VIEW_PORT_TILES_W, VIEW_PORT_TILES_H


class Game:
    def __init__(self):
        pygame.init()
        current_max_dim = self.get_max_dimension()
        self.screen = pygame.display.set_mode(
            (current_max_dim - 1 / 6 * current_max_dim, current_max_dim - 1 / 6 * current_max_dim))
        self.scale_factor = math.ceil(current_max_dim / TILE_WIDTH / VIEW_PORT_TILES_W)
        self.tmx_data = load_pygame("src/tiles/level_1.tmx")
        self.scale_grid()
        self.current_start_pos_x = 800
        self.current_start_pos_y = 100
        self.movement_speed = 0.7

    @staticmethod
    def get_max_dimension():
        display_info = pygame.display.Info()
        native_width, native_height = display_info.current_w, display_info.current_h
        current_max_dim = min(native_height, native_width)
        return current_max_dim

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

    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a] and not self.collide_with_block(
                self.current_start_pos_x - self.movement_speed,
                self.current_start_pos_y):
            self.current_start_pos_x -= self.movement_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and not self.collide_with_block(
                self.current_start_pos_x + self.movement_speed,
                self.current_start_pos_y):
            self.current_start_pos_x += self.movement_speed
        if keys[pygame.K_UP] or keys[pygame.K_w] and not self.collide_with_block(self.current_start_pos_x,
                                                                                 self.current_start_pos_y - self.movement_speed):
            self.current_start_pos_y -= self.movement_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s] and not self.collide_with_block(self.current_start_pos_x,
                                                               self.current_start_pos_y + self.movement_speed):
            self.current_start_pos_y += self.movement_speed

    def collide_with_block(self, new_x, new_y):
        player_map_x = int((self.screen.get_width() / 2 / self.scale_factor + new_x) // TILE_WIDTH)
        player_map_y = int((self.screen.get_height() / 2 / self.scale_factor + new_y) // TILE_HEIGHT)

        result = self.get_tile_properties(player_map_x, player_map_y, self.tmx_data.layers[-1])
        return result and result["is_block"]

    def render_map(self):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, tile in layer.tiles():
                    if self.current_start_pos_x - TILE_WIDTH <= x * TILE_WIDTH <= self.current_start_pos_x + VIEW_PORT_TILES_W * TILE_WIDTH + TILE_WIDTH \
                            and self.current_start_pos_y - TILE_WIDTH <= y * TILE_HEIGHT <= self.current_start_pos_y + VIEW_PORT_TILES_H * TILE_HEIGHT + TILE_WIDTH:
                        screen_x = (x * TILE_WIDTH - self.current_start_pos_x) * self.scale_factor
                        screen_y = (y * TILE_HEIGHT - self.current_start_pos_y) * self.scale_factor
                        self.screen.blit(tile, (screen_x, screen_y))

    def update(self):
        self.move_player()
        self.render_map()
        pygame.draw.circle(self.screen, (255, 0, 0), (self.screen.get_width() / 2, self.screen.get_height() / 2), 20)

    def get_tile_properties(self, x, y, layer):
        if layer and hasattr(layer, 'tiles'):
            gid = layer.data[y][x]
            properties = self.tmx_data.get_tile_properties_by_gid(gid)
            return properties
        return None


if __name__ == "__main__":
    game = Game()
    game.run()
