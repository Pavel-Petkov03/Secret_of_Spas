from pygame_menu import Menu


class BaseMenu:
    def __init__(self, title, width, height, *args, **kwargs):
        self._menu = Menu(title, width, height, *args, **kwargs)
