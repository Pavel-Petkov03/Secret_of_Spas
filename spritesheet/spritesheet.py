import pygame
import settings


class SpriteSheet:
    def __init__(self, filename, rows, cols):
        """
        Initialize the sprite sheet by loading the image and calculating
        the position of each sprite frame.
        """
        self.filename = filename
        self.rows = rows
        self.cols = cols
        self.sheet = pygame.image.load(self.filename).convert_alpha()
        self.frame_width = self.sheet.get_width() // self.cols
        self.frame_height = self.sheet.get_height() // self.rows
        self._matrix = self._generate_sprite_sheet_matrix()

    def _generate_sprite_sheet_matrix(self):
        matrix = []
        for row in range(self.rows):
            row_sprites = []
            for col in range(self.cols):
                x = col * self.frame_width
                y = row * self.frame_height
                sprite = self.sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                sprite = pygame.transform.scale(sprite, (self.frame_width * settings.SCALE_FACTOR, self.frame_height * settings.SCALE_FACTOR))
                row_sprites.append(sprite)
            matrix.append(row_sprites)
        return matrix

    @property
    def matrix(self):
        return self._matrix

