import math
import random
import pygame
from pytmx.util_pygame import load_pygame
import settings
from car.car_display import Car
from decorators.is_in_blit_range import IsInBlitRange
from events.base_event import EventManager
from events.redirect_event import ShowRedirectToAnotherMapEvent, ShowMissionEvent
from item_inventory.inventory import Inventory
from player.utils import init_player, enemy_factory
from snitches.settings import Spas, SNITCHES
from spritesheet.utils import get_animation_matrix


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH,
             settings.SCREEN_WIDTH)
        )
        self.clock = pygame.time.Clock()
        self.dungeon = None
        self.available_snitches = set()
        self.available_snitches.add(Spas)
        self.change_dungeon("village", is_village=True)
        self.fps = 60

    def run(self):
        running = True
        while running:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    running = False
                EventManager.handle_event(event, self)
            delta_time = self.clock.tick(self.fps)
            self.screen.fill((255, 0, 0))
            self.update(delta_time, event_list)
            self.dungeon.blit(self.screen)
            pygame.display.update()
            pygame.display.flip()

    def update(self, delta_time, event_list):
        self.dungeon.update(self.screen, delta_time, event_list, self.additional_kwargs())

    def change_dungeon(self, dungeon_name, is_village=False):
        create_class = Village if is_village else Dungeon
        self.dungeon = create_class(dungeon_name)
        self.dungeon.player.x, self.dungeon.player.y = settings.PLAYER_POS_DUNGEON_LOGGER[dungeon_name]

    def additional_kwargs(self):
        return {
            "available_snitches": self.available_snitches
        }


class BaseDungeon:
    DUNGEON_FOLDER_DIR = "src/tile_maps/"
    is_shooting_allowed = None

    def __init__(self, dungeon_name):
        self.name = dungeon_name
        self.tmx_data = load_pygame(self.DUNGEON_FOLDER_DIR + dungeon_name + ".tmx")
        self.scale_grid()
        self.player = init_player(self)
        self.items = []
        self.inventory = Inventory()
        self.popup_menu = None

    def scale_grid(self):
        for gid, image in enumerate(self.tmx_data.images):
            if image is not None:
                new_width = image.get_width() * settings.SCALE_FACTOR
                new_height = image.get_height() * settings.SCALE_FACTOR
                scaled_image = pygame.transform.scale(image, (new_width, new_height))
                self.tmx_data.images[gid] = scaled_image

    def update(self, screen, delta_time, event_list, additional_kwargs):
        self.handle_events(screen, additional_kwargs)
        self.player.update(screen, delta_time, event_list, is_shooting_allowed=self.is_shooting_allowed)
        if self.popup_menu:
            self.popup_menu.update(event_list)

    def handle_events(self, screen, additional_kwargs):
        if (snitch_data := self.player.collides_with_snitch(screen)) and not self.popup_menu:
            available_snitches = additional_kwargs["available_snitches"]
            snitch_name = snitch_data["snitch_name"]
            if self.is_snitch_available(available_snitches, snitch_name):
                current_event = ShowMissionEvent(additional_state={
                    "snitch_name": snitch_name,
                    "inventory": self.inventory,
                    "available_snitches": available_snitches
                }, dungeon_state=self)
                current_event.start()
        elif (gate_data := self.player.collides_with_gate(screen)) and not self.popup_menu:
            current_event = ShowRedirectToAnotherMapEvent(additional_state=gate_data, dungeon_state=self)
            current_event.start()

    def is_snitch_available(self, available_snitches, name):
        return SNITCHES[name] in available_snitches

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
        self.items = []

    def blit(self, screen):
        self.render_map(screen)
        for enemy in self.enemies:
            enemy.blit(screen)
        self.player.blit(screen)
        if self.popup_menu:
            self.popup_menu.draw(screen)
        for item in self.items:
            item.blit(screen)
        self.inventory.blit(screen)

    def update(self, screen, delta_time, event_list, additional_data):
        super().update(screen, delta_time, event_list, additional_data)
        self.update_inventory(screen, event_list)
        for enemy in self.enemies:
            enemy.update(screen, delta_time, event_list)

    def update_inventory(self, screen, event_list):
        for item in self.items:
            if item.get_distance_to_player(screen) < 1:
                self.items.remove(item)
                self.inventory.add_item(item)
                break
        self.inventory.menu.update(event_list)


class Village(BaseDungeon):
    is_shooting_allowed = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        animation_frames = get_animation_matrix("car_movement")
        result = [
            [animation_frames[0][1]],
            [animation_frames[0][3]],
            [animation_frames[0][5]],
            [animation_frames[0][7]],
        ]
        self.car = Car(1200, 400, result[0], result, self)

    def update(self, screen, delta_time, event_list, additional_data):
        self.inventory.menu.update(event_list)
        self.update_car(screen, delta_time, event_list, additional_data)
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f and self.distance_between_car_and_player(
                    screen) < 3:
                self.car.is_mount = not self.car.is_mount
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n and self.car.is_mount:
                self.car.change_stream()

    def distance_between_car_and_player(self, screen):
        x1, y1 = self.player.get_map_position(screen)
        x2, y2 = self.car.get_map_position(screen)
        return int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))

    def update_car(self, screen, delta_time, event_list, additional_data):
        if self.car.is_player_in_car():
            self.car.handle_player_in_car()
            self.car.update(screen, delta_time, event_list)
            self.player.change_pos(*self.car.get_x_y_pos())
        else:
            self.car.handle_player_out_of_car()
            super().update(screen, delta_time, event_list, additional_data)

    def blit(self, screen):
        self.render_map(screen)
        self.car.blit(screen)
        if not self.car.is_mount:
            self.player.blit(screen)
        if self.popup_menu:
            self.popup_menu.draw(screen)
        self.inventory.blit(screen)


if __name__ == "__main__":
    game = Game()
    game.run()
