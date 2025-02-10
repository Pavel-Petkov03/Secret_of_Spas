from abc import ABC, abstractmethod
import pygame


class Event(ABC):
    def __init__(self, event_type, dungeon_state=None, additional_state=None):
        self.event_type = event_type
        self.dungeon_state = dungeon_state
        self.additional_state = additional_state
        self.start_event()

    @abstractmethod
    def run_event_listener(self, game_state):
        pass

    def start_event(self):
        if self.additional_state:
            custom_event = pygame.event.Event(self.event_type, self.additional_state)
        else:
            custom_event = pygame.event.Event(self.event_type)
        pygame.event.post(custom_event)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class EventManager(metaclass=SingletonMeta):
    events = {}

    @classmethod
    def register_event(cls, custom_event: Event):
        cls.events[custom_event.event_type] = custom_event

    @classmethod
    def handle_event(cls, event, game_state):
        if event.type in cls.events:
            cls.events[event.type].run_event_listener(game_state)
