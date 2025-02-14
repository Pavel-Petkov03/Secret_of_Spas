import pygame

from settings import SCREEN_WIDTH


class HealthBar:
    PADDING_RATIO = 0.02

    def __init__(self, player):
        self.player = player
        self.width = SCREEN_WIDTH / 4
        self.height = SCREEN_WIDTH / 12
        self.x = (SCREEN_WIDTH - self.width) / 2
        self.y = SCREEN_WIDTH - self.height - SCREEN_WIDTH * self.PADDING_RATIO

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width * (self.player.health / 100), self.height))
