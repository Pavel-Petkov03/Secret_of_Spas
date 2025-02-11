import pygame_menu

import settings
from events.base_event import Event, EventManager
from events.event_types.dungeos import REDIRECT_TO_ANOTHER_MAP
from events.event_types.modals import REDIRECT_MODAL_EVENT
from settings import GATE_LEVEL_INFO


class RedirectEvent(Event):
    event_type = REDIRECT_TO_ANOTHER_MAP

    def run_event_listener(self, game_state):
        # todo create to village redirect
        url = self.additional_state["redirect_url"]
        game_state.change_dungeon(url, is_village=True if url == settings.VILLAGE_URL else False
                                  )


class ShowRedirectToAnotherMapEvent(Event):
    event_type = REDIRECT_MODAL_EVENT

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
        current_event = RedirectEvent(additional_state=self.additional_state)
        current_event.start()
