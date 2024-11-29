import pygame
import pygame_menu
from pytmx.util_pygame import load_pygame
import settings
from player.utils import init_player, init_enemy


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH,
             settings.SCREEN_WIDTH)
        )
        self.tmx_data = load_pygame("src/tile_maps/first_level.tmx")
        self.scale_grid()
        self.clock = pygame.time.Clock()
        self.player = init_player(self.tmx_data)
        self.enemies = [init_enemy("Gosho", 100, 100, self.player, self.tmx_data) for _ in range(50)]
        self.fps = 60
        # self.menu = pygame_menu.Menu("Settings", 200, 300)
        # self.menu.add.range_slider("Background", 50, (0, 100), increment=1, width=1)
        # self.menu.add.button("Yes")
        # self.menu.add.button("No")


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
            delta_time = self.clock.tick(self.fps)
            self.update(delta_time / 1000)
            for enemy in self.enemies:
                enemy.blit(self.screen)
            self.player.blit(self.screen)
            # self.menu.update(pygame.event.get())
            # self.menu.draw(self.screen)
            pygame.display.update()
            pygame.display.flip()

    def render_map(self):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, tile in layer.tiles():
                    if self.player.x - settings.TILE_WIDTH <= x * settings.TILE_WIDTH <= self.player.x + settings.VIEW_PORT_TILES_W * settings.TILE_WIDTH + settings.TILE_WIDTH \
                            and self.player.y - settings.TILE_WIDTH <= y * settings.TILE_HEIGHT <= self.player.y + settings.VIEW_PORT_TILES_H * settings.TILE_HEIGHT + settings.TILE_WIDTH:
                        screen_x = (x * settings.TILE_WIDTH - self.player.x) * settings.SCALE_FACTOR
                        screen_y = (y * settings.TILE_HEIGHT - self.player.y) * settings.SCALE_FACTOR
                        self.screen.blit(tile, (screen_x, screen_y))

    def update(self, delta_time):
        self.player.update(self.screen, delta_time)
        self.render_map()
        for enemy in self.enemies:
            enemy.update(self.screen, delta_time)


if __name__ == "__main__":
    game = Game()
    game.run()
