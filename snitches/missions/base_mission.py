import pygame
import settings
import pygame_menu


class Mission:
    def __init__(self, text_rows, image_url, label="Mission"):
        self.image_url = image_url
        self.text_rows = text_rows
        self.label = label
        self.menu = pygame_menu.Menu(self.label, settings.SCREEN_WIDTH / 2, settings.SCREEN_WIDTH / 2,
                                     theme=pygame_menu.themes.THEME_DARK)
        self.menu.add.image(self.image_url, scale=(settings.SCALE_FACTOR / 10, settings.SCALE_FACTOR / 10))
        self.menu.add.label("Vili the keeper", font_size=int(settings.SCALE_FACTOR * 20))
        self.menu.add.label("", font_size=int(settings.SCALE_FACTOR * 20))
        for text in text_rows:
            self.menu.add.label(text, font_size=int(settings.SCALE_FACTOR*15))
            self.menu.add.button("Done", background_color=(255, 0, 0))

    def blit(self, screen):
        self.menu.draw(screen)
