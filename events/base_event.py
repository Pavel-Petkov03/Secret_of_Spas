from abc import ABC, abstractmethod
import pygame

from utils.singeton_meta import SingletonMeta


class Event(ABC):
    event_type = None

    def __init__(self, dungeon_state=None, additional_state=None):
        self.dungeon_state = dungeon_state
        self.additional_state = additional_state

    @abstractmethod
    def run_event_listener(self, game_state):
        pass

    def start(self):
        if self.additional_state:
            custom_event = pygame.event.Event(self.event_type, self.additional_state)
        else:
            custom_event = pygame.event.Event(self.event_type)
        pygame.event.post(custom_event)
        EventManager.register_event(self)


class EventManager(metaclass=SingletonMeta):
    events = {}

    @classmethod
    def register_event(cls, custom_event: Event):
        cls.events[custom_event.event_type] = custom_event

    @classmethod
    def handle_event(cls, event, game_state):
        if event.type in cls.events:
            cls.events[event.type].run_event_listener(game_state)
