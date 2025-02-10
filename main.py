import math
import random
import events.event_types.dungeos as dungeon_events
import events.event_types.modals as modal_events
import pygame
from pytmx.util_pygame import load_pygame
import settings
from car.car_display import Car
from decorators.is_in_blit_range import IsInBlitRange
from errors import RedirectToVillageError
from events.base_event import EventManager
from events.redirect_event import RedirectEvent, ShowRedirectToAnotherMapEvent
from player.utils import init_player, enemy_factory
from snitches.missions.base_mission import Mission
from spritesheet.utils import get_animation_matrix


class Game:
    DUNGEON_FOLDER_DIR = "src/tile_maps/"

    def __init__(self):
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH,
             settings.SCREEN_WIDTH)
        )
        self.clock = pygame.time.Clock()
        self.dungeon = None
        self.change_dungeon("village", is_village=True)
        self.fps = 60
        self.mission = Mission(["Take 1000 water droplets", "qga", "Kill 100 archers", "Come back to me"],
                               "src/images/blonde_girl.png")

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
            # self.mission.menu.draw(self.screen)
            pygame.display.update()
            pygame.display.flip()

    def update(self, delta_time, event_list):
        try:
            self.dungeon.update(self.screen, delta_time, event_list)
            # self.mission.menu.update(event_list)
        except RedirectToVillageError:
            self.change_dungeon("village", is_village=True)

    def change_dungeon(self, dungeon_name, is_village=False):
        create_class = Village if is_village else Dungeon
        self.dungeon = create_class(self.DUNGEON_FOLDER_DIR + dungeon_name + ".tmx")
        self.dungeon.player.x, self.dungeon.player.y = settings.PLAYER_POS_DUNGEON_LOGGER[dungeon_name]


class BaseDungeon:
    is_shooting_allowed = None

    def __init__(self, tmx_string):
        self.tmx_data = load_pygame(tmx_string)
        self.scale_grid()
        self.player = init_player(self)
        self.popup_menu = None

    def scale_grid(self):
        for gid, image in enumerate(self.tmx_data.images):
            if image is not None:
                new_width = image.get_width() * settings.SCALE_FACTOR
                new_height = image.get_height() * settings.SCALE_FACTOR
                scaled_image = pygame.transform.scale(image, (new_width, new_height))
                self.tmx_data.images[gid] = scaled_image

    def update(self, screen, delta_time, event_list):
        self.handle_events(screen)
        self.player.update(screen, delta_time, event_list, is_shooting_allowed=self.is_shooting_allowed)
        if self.popup_menu:
            self.popup_menu.update(event_list)

    def handle_events(self, screen):
        if snitch_data := self.player.collides_with_snitch(screen):
            # current_event = ShowRedirectToAnotherMapEvent(modal_events.REDIRECT_MODAL_EVENT, additional_state={
            #     "redirect_url" : snitch_data[]
            # })
            pass
        elif (gate_data := self.player.collides_with_gate(screen)) and not self.popup_menu:
            print(gate_data)
            current_event = ShowRedirectToAnotherMapEvent(modal_events.REDIRECT_MODAL_EVENT, additional_state=gate_data,
                                                          dungeon_state=self)
            EventManager.register_event(current_event)

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
        if self.popup_menu:
            self.popup_menu.draw(screen)

    def update(self, screen, delta_time, event_list):
        super().update(screen, delta_time, event_list)
        for enemy in self.enemies:
            enemy.update(screen, delta_time, event_list)


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

    def update(self, screen, delta_time, event_list):
        self.update_car(screen, delta_time, event_list)
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

    def update_car(self, screen, delta_time, event_list):
        if self.car.is_player_in_car():
            self.car.handle_player_in_car()
            self.car.update(screen, delta_time, event_list)
            self.player.change_pos(*self.car.get_x_y_pos())
        else:
            self.car.handle_player_out_of_car()
            super().update(screen, delta_time, event_list)

    def blit(self, screen):
        self.render_map(screen)
        self.car.blit(screen)
        if not self.car.is_mount:
            self.player.blit(screen)
        if self.popup_menu:
            self.popup_menu.draw(screen)


if __name__ == "__main__":
    game = Game()
    game.run()
