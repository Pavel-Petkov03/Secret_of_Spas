import math

import pygame.image
import pygame_menu

import settings
from decorators.is_in_blit_range import IsInBlitRange


class Inventory:
    def __init__(self):
        self.items = {}
        self.menu = pygame_menu.Menu("Inventory", settings.SCREEN_WIDTH / 4, settings.SCREEN_WIDTH / 4)
        self.menu.set_relative_position(0, 0)

    def add_item(self, item):
        if item.name in self.items:
            self.items[item.name] += 1
        else:
            self.items[item.name] = 1

    def blit(self, screen):
        menu = pygame_menu.Menu("Inventory", settings.SCREEN_WIDTH / 4, settings.SCREEN_WIDTH / 4)
        menu.set_relative_position(0, 0)
        for item_name, count in self.items.items():
            menu.add.label(f"{item_name}: {count}")
        self.menu.draw(screen)


class Item:
    def __init__(self, x, y, name, image_url, player):
        self.x = x
        self.y = y
        self.name = name
        self.image = self.load_image(image_url)
        self.player = player

    @staticmethod
    def load_image(image_url):
        image = pygame.image.load(image_url)
        new_width = image.get_width() * settings.SCALE_FACTOR / 2
        new_height = image.get_height() * settings.SCALE_FACTOR / 2
        return pygame.transform.scale(image, (new_width, new_height))

    def blit(self, screen):
        self.__blit(self.x, self.y, screen, self.image)

    @IsInBlitRange
    def __blit(self, x, y, screen, image):
        screen_x = (x - self.player.x) * settings.SCALE_FACTOR
        screen_y = (y - self.player.y) * settings.SCALE_FACTOR
        screen_x = (2 * screen_x - image.get_width()) / 2
        screen_y = (2 * screen_y - image.get_height()) / 2
        screen.blit(image, (screen_x, screen_y))

    def get_map_position(self, screen):
        tile_x = self.x // settings.TILE_WIDTH
        tile_y = self.y // settings.TILE_WIDTH
        return tile_x, tile_y

    def get_distance_to_player(self, screen):
        current_tile_x, current_tile_y = self.get_map_position(screen)
        main_player_x, main_player_y = self.player.get_map_position(screen)
        dx = current_tile_x - main_player_x
        dy = current_tile_y - main_player_y
        return math.sqrt(dx ** 2 + dy ** 2)
