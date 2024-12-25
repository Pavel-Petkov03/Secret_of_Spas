import random

import pygame
from pytmx.util_pygame import load_pygame
import settings
from decorators.is_in_blit_range import IsInBlitRange
from player.utils import init_player, enemy_factory
from errors import RedirectToVillageError, DeadError


class Game:
    DUNGEON_FOLDER_DIR = "src/tile_maps/"

    def __init__(self):
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH,
             settings.SCREEN_WIDTH)
        )
        self.clock = pygame.time.Clock()
        self.dungeon = Dungeon("src/tile_maps/first_level.tmx")
        self.fps = 60

    def run(self):
        running = True
        while running:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    running = False
            delta_time = self.clock.tick(self.fps)
            self.screen.fill((255, 0, 0))
            self.update(delta_time, event_list)
            self.dungeon.blit(self.screen)
            pygame.display.update()
            pygame.display.flip()

    def update(self, delta_time, event_list):
        try:
            self.dungeon.update(self.screen, delta_time, event_list)
        except RedirectToVillageError:
            self.change_dungeon("village", is_village=True)
            self.dungeon.player.x, self.dungeon.player.y = settings.PLAYER_POS_DUNGEON_LOGGER["village"]

    def change_dungeon(self, dungeon_name, is_village=False):
        create_class = Village if is_village else Dungeon
        self.dungeon = create_class(self.DUNGEON_FOLDER_DIR + dungeon_name + ".tmx")


class BaseDungeon:
    is_shooting_allowed = None

    def __init__(self, tmx_string):
        self.tmx_data = load_pygame(tmx_string)
        self.scale_grid()
        self.player = init_player(self)

    def scale_grid(self):
        for gid, image in enumerate(self.tmx_data.images):
            if image is not None:
                new_width = image.get_width() * settings.SCALE_FACTOR
                new_height = image.get_height() * settings.SCALE_FACTOR
                scaled_image = pygame.transform.scale(image, (new_width, new_height))
                self.tmx_data.images[gid] = scaled_image

    def update(self, screen, delta_time, event_list):
        self.player.update(screen, delta_time, event_list, is_shooting_allowed=self.is_shooting_allowed)

    def blit(self, screen):
        self.render_map(screen)
        self.player.blit(screen)

    def render_map(self, screen):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, tile in layer.tiles():
                    self.blit_tile(x * settings.TILE_WIDTH, y * settings.TILE_WIDTH, screen, tile)

    @IsInBlitRange
    def blit_tile(self, x, y, screen, tile):
        screen_x = (x - self.player.x) * settings.SCALE_FACTOR
        screen_y = (y - self.player.y) * settings.SCALE_FACTOR
        screen.blit(tile, (screen_x, screen_y))


class Dungeon(BaseDungeon):
    is_shooting_allowed = True

    def __init__(self, tmx_string):
        super().__init__(tmx_string)
        self.enemies = [enemy_factory("Gosho", 100, 100, self, random.choice([True, False])) for _ in range(50)]

    def blit(self, screen):
        self.render_map(screen)
        for enemy in self.enemies:
            enemy.blit(screen)
        self.player.blit(screen)

    def update(self, screen, delta_time, event_list):
        super().update(screen, delta_time, event_list)
        for enemy in self.enemies:
            enemy.update(screen, delta_time, event_list)


class Village(BaseDungeon):
    is_shooting_allowed = False


if __name__ == "__main__":
    game = Game()
    game.run()
