from abc import ABC, abstractmethod
from enum import Enum
import pygame_menu
import settings

IMAGE_URLS = {
    "Vili": "src/images/snitches_pictures/Vili.png",
    "Spas": "src/images/snitches_pictures/Spas.png",
    "Eva": "src/images/snitches_pictures/Eva.png",
    "Vladi": "src/images/snitches_pictures/Vladi.png"
}

SNITCH_TARGET_DUNGEONS = {
    "Spas": "first_level",
    "Vili": "second_level",
    "Eva": "third_level",
    "Vladi": "fourth_level"
}


class MissionState(Enum):
    NOT_TAKEN = 1
    IN_PROGRESS = 2


class BaseMission(ABC):
    TITLE_FONT_SIZE = int(settings.SCREEN_WIDTH / 2 * 0.12)
    LABEL_FONT_SIZE = int(settings.SCREEN_WIDTH / 2 * 0.08)

    def __init__(self, snitch):
        self.snitch = snitch

    @abstractmethod
    def get_modal(self, **kwargs):
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title_font_size = self.TITLE_FONT_SIZE
        menu = pygame_menu.Menu("Mission", settings.SCREEN_WIDTH / 2, settings.SCREEN_WIDTH / 2,
                                theme=pygame_menu.themes.THEME_DARK)
        menu.add.label(f"{kwargs['snitch_name']} the keeper", font_size=self.LABEL_FONT_SIZE)
        menu.add.image(IMAGE_URLS[self.snitch.name],
                       scale=(settings.SCALE_FACTOR / 10, settings.SCALE_FACTOR / 10))
        return menu


class ActionMission(BaseMission):

    def __init__(self, snitch, ingredient_name, ingredient_quantity):
        super().__init__(snitch)
        self.state = MissionState.NOT_TAKEN
        self.ingredient_name = ingredient_name
        self.ingredient_quantity = ingredient_quantity

    def get_mission_place_string(self):
        return f"You have to go to {SNITCH_TARGET_DUNGEONS[self.snitch.name]}"

    def get_mission_target_string(self):
        return f"And take {self.ingredient_quantity} {self.ingredient_name}"

    def is_done(self, inventory):
        return self.ingredient_name in inventory.items and inventory.items[
            self.ingredient_name] >= self.ingredient_quantity

    def get_modal(self, **kwargs):
        menu = super().get_modal(**kwargs)
        menu.add.label(self.get_mission_place_string(), font_size=self.LABEL_FONT_SIZE)
        menu.add.label(self.get_mission_target_string(), font_size=self.LABEL_FONT_SIZE)
        menu.add.label("", font_size=self.LABEL_FONT_SIZE)
        if self.state == MissionState.NOT_TAKEN:
            menu.add.button("Accept", lambda: self.accept_mission(kwargs["dungeon_state"]))
        elif self.is_done(kwargs["inventory"]):
            menu.add.button("Done", lambda: self.mission_done(kwargs["dungeon_state"], kwargs["inventory"]))
        elif self.state == MissionState.IN_PROGRESS:
            menu.add.button("Continue", lambda: self.accept_mission(kwargs["dungeon_state"]))
        return menu

    def accept_mission(self, dungeon_state):
        dungeon_state.popup_menu = None
        self.state = MissionState.IN_PROGRESS

    @staticmethod
    def continue_mission(dungeon_state):
        dungeon_state.popup_menu = None

    def mission_done(self, dungeon_state, inventory):
        dungeon_state.popup_menu = None
        inventory.remove_items_from_mission(self)
        self.snitch.change_mission()


class InfoMessage(BaseMission):
    MAX_WORD_COUNT_ON_ROW = 4

    def __init__(self, snitch, text):
        super().__init__(snitch)
        self.text = text

    def get_modal(self, **kwargs):
        menu = super().get_modal(**kwargs)
        for text_row in self.group_words():
            string_row = "".join(text_row)
            menu.add.label(string_row, font_size=self.LABEL_FONT_SIZE)
        menu.add.button("Continue", lambda: self.continue_mission(kwargs["dungeon_state"]))
        return menu

    def group_words(self):
        words = self.text.split()
        grouped = [' '.join(words[i:i + self.MAX_WORD_COUNT_ON_ROW]) for i in
                   range(0, len(words), self.MAX_WORD_COUNT_ON_ROW)]
        return grouped

    def continue_mission(self, dungeon_state):
        self.snitch.change_mission()
        dungeon_state.popup_menu = None



class EndOfMissionsMessage(BaseMission):
    def get_modal(self, **kwargs):
        menu = super().get_modal(**kwargs)
        menu.add.label("This is the information I know", font_size=self.LABEL_FONT_SIZE)
        menu.add.label(f"Go to {self.snitch.next_snitch.name}", font_size=self.LABEL_FONT_SIZE)
        menu.add.button("Continue",
                        lambda: self.continue_mission(kwargs["dungeon_state"], kwargs["available_snitches"]))
        return menu

    def continue_mission(self, dungeon_state, available_snitches):
        available_snitches.add(self.snitch.next_snitch)
        dungeon_state.popup_menu = None
