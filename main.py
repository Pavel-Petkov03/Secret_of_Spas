import pygame
import settings
from dungeon import Village, Dungeon
from events.base_event import EventManager
from snitches.settings import Spas


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


if __name__ == "__main__":
    game = Game()
    game.run()
