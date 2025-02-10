import pygame_menu


class RedirectMenu:
    def __init__(self):
        self.menu = pygame_menu.Menu("Do you want to redirect to",
                                     100,
                                     100,
                                     )
        self.menu.add.label("Pri gosho")
        self.menu.add.image("bla bla")
        self.menu.add.button("Yes", action=None)
        self.menu.add.button("No", action=None)