import pygame_menu

import settings
from events.base_event import Event, EventManager
from events.event_types.dungeos import REDIRECT_TO_ANOTHER_MAP
from events.event_types.modals import REDIRECT_MODAL_EVENT
from settings import GATE_LEVEL_INFO
import snitches.settings as snitch_info

class RedirectEvent(Event):
    event_type = REDIRECT_TO_ANOTHER_MAP

    def run_event_listener(self, game_state):
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


class ShowMissionEvent(Event):
    def draw_modal(self, inventory):
        current_snitch = snitch_info.SNITCHES[self.additional_state["name"]]
        current_mission = current_snitch.missions[0]

        menu = pygame_menu.Menu("Mission", settings.SCREEN_WIDTH / 2, settings.SCREEN_WIDTH / 2,
                                theme=pygame_menu.themes.THEME_DARK)
        menu.add.label(f"{self.additional_state['name']} the keeper", font_size=int(settings.SCALE_FACTOR * 20))
        menu.add.image(snitch_info.IMAGE_URLS[self.additional_state['name']], scale=(settings.SCALE_FACTOR / 10, settings.SCALE_FACTOR / 10))
        menu.add.label("", font_size=int(settings.SCALE_FACTOR * 20))
        if len(self.missions) == 1:
            pass
        else:
            self.draw_mission(menu, current_mission)

    def draw_mission(self, menu, current_mission):
        menu.add.label(current_mission.get_mission_place_string(self.additional_state['name']),
                       font_size=int(settings.SCALE_FACTOR * 15))
        menu.add.label(current_mission.get_mission_target_string(), font_size=int(settings.SCALE_FACTOR * 15))
        if current_mission.state == MissionState.NOT_TAKEN:
            menu.add.button("Accept", lambda: self.accept_mission(current_mission))
        elif current_mission.state == MissionState.IN_PROGRESS:
            menu.add.button("Continue", lambda: self.accept_mission)

    def accept_mission(self, current_mission):
        current_mission.state = MissionState.IN_PROGRESS
        self.dungeon_state.popup_menu = None

    def

