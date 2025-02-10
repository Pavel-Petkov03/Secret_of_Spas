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
        self.image = pygame.image.load(image_url)
        self.image = pygame.transform.scale(self.image, (settings.SCALE_FACTOR, settings.SCALE_FACTOR))
        self.player = player

    def blit(self, screen):
        self.__blit(self.x, self.y, screen, self.image)

    @IsInBlitRange
    def __blit(self, x, y, screen, image):
        screen_x = (x - self.player.x) * settings.SCALE_FACTOR
        screen_y = (y - self.player.y) * settings.SCALE_FACTOR
        screen_x = (2 * screen_x - image.get_width()) / 2
        screen_y = (2 * screen_y - image.get_height()) / 2
        screen.blit(image, (screen_x, screen_y))
