import pygame_menu

import settings
from events.base_event import Event, EventManager
from events.event_types.dungeos import REDIRECT_TO_ANOTHER_MAP
from settings import GATE_LEVEL_INFO


class RedirectEvent(Event):
    def run_event_listener(self, game_state):
        # todo create to village redirect
        game_state.change_dungeon(self.additional_state["redirect_url"], is_village=False)


class ShowRedirectToAnotherMapEvent(Event):

    def run_event_listener(self, game_state):
        self.dungeon_state.popup_menu = self.create_menu()

    def create_menu(self):
        modal = pygame_menu.Menu(
            "Do you want to go to",
            settings.SCREEN_WIDTH / 2, settings.SCREEN_WIDTH / 2,
            theme=pygame_menu.themes.THEME_DARK
        )
        props = GATE_LEVEL_INFO[self.additional_state["redirect_url"]]
        modal.add.label(props["village_name"])
        modal.add.image(props["village_image_location"], scale=(settings.SCALE_FACTOR / 5, settings.SCALE_FACTOR / 5))
        modal.add.button("No", self.remove_modal)
        modal.add.button("Yes", self.redirect)
        return modal

    def remove_modal(self):
        self.dungeon_state.popup_menu = None

    def redirect(self):
        current_event = RedirectEvent(REDIRECT_TO_ANOTHER_MAP, additional_state=self.additional_state)
        EventManager.register_event(current_event)
