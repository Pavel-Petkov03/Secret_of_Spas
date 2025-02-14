import pygame_menu

import settings
from events.base_event import Event, EventManager
from events.event_types.dungeos import REDIRECT_TO_ANOTHER_MAP
from events.event_types.modals import REDIRECT_MODAL_EVENT, SHOW_SNITCH_MODAL_EVENT
from settings import GATE_LEVEL_INFO
import snitches.settings as snitch_info


class RedirectEvent(Event):
    event_type = REDIRECT_TO_ANOTHER_MAP

    def run_event_listener(self, game_state):
        url = self.additional_state["redirect_url"]
        game_state.change_dungeon(url, is_village=True if url == settings.VILLAGE_URL else False)


class ShowRedirectToAnotherMapEvent(Event):
    event_type = REDIRECT_MODAL_EVENT
    TITLE_FONT_SIZE = int(settings.SCREEN_WIDTH / 2 * 0.1)
    LABEL_FONT_SIZE = int(settings.SCREEN_WIDTH / 2 * 0.08)

    def run_event_listener(self, game_state):
        self.dungeon_state.popup_menu = self.create_menu()

    def create_menu(self):
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title_font_size = self.TITLE_FONT_SIZE
        modal = pygame_menu.Menu(
            "Do you want to go to",
            settings.SCREEN_WIDTH / 2, settings.SCREEN_WIDTH / 2,
            theme=theme,
        )
        props = GATE_LEVEL_INFO[self.additional_state["redirect_url"]]
        modal.add.label(props["village_name"], font_size=self.LABEL_FONT_SIZE)
        modal.add.image(props["village_image_location"], scale=(settings.SCALE_FACTOR / 10, settings.SCALE_FACTOR / 10))
        modal.add.button("No", self.remove_modal)
        modal.add.button("Yes", self.redirect)
        return modal

    def remove_modal(self):
        self.dungeon_state.popup_menu = None

    def redirect(self):
        current_event = RedirectEvent(additional_state=self.additional_state)
        current_event.start()


class ShowMissionEvent(Event):
    event_type = SHOW_SNITCH_MODAL_EVENT

    def run_event_listener(self, game_state):
        current_snitch = snitch_info.SNITCHES[self.additional_state["snitch_name"]]
        mission = current_snitch.get_current_mission()
        modal = mission.get_modal(
            inventory=self.additional_state["inventory"],
            dungeon_state=self.dungeon_state,
            snitch_name=self.additional_state["snitch_name"],
            available_snitches=self.additional_state["available_snitches"]
        )
        self.dungeon_state.popup_menu = modal
