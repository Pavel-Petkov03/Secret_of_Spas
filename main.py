import pygame
from pytmx.util_pygame import load_pygame
import settings
from player.utils import init_player


class Game:
    def __init__(self):
        self.screen = settings.SCREEN
        self.tmx_data = load_pygame("src/tiles/level_1.tmx")
        self.scale_grid()
        self.clock = pygame.time.Clock()
        self.player = init_player(self.tmx_data)
        self.enemies = []

    def scale_grid(self):
        for gid, image in enumerate(self.tmx_data.images):
            if image is not None:
                new_width = image.get_width() * settings.SCALE_FACTOR
                new_height = image.get_height() * settings.SCALE_FACTOR
                scaled_image = pygame.transform.scale(image, (new_width, new_height))
                self.tmx_data.images[gid] = scaled_image

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            self.player.blit(self.screen)
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(60)

    def render_map(self):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, tile in layer.tiles():
                    if self.player.x - settings.TILE_WIDTH <= x * settings.TILE_WIDTH <= self.player.x + settings.VIEW_PORT_TILES_W * settings.TILE_WIDTH + settings.TILE_WIDTH \
                            and self.player.y - settings.TILE_WIDTH <= y * settings.TILE_HEIGHT <= self.player.y + settings.VIEW_PORT_TILES_H * settings.TILE_HEIGHT + settings.TILE_WIDTH:
                        screen_x = (x * settings.TILE_WIDTH - self.player.x) * settings.SCALE_FACTOR
                        screen_y = (y * settings.TILE_HEIGHT - self.player.y) * settings.SCALE_FACTOR
                        self.screen.blit(tile, (screen_x, screen_y))

    def update(self):
        self.player.update(self.screen)
        self.render_map()
        print(self.player.x, self.player.y)


if __name__ == "__main__":
    game = Game()
    game.run()
