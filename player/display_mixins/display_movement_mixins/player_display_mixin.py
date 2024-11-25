import settings
from player.display_mixins.display_movement_mixins.base_display_character_mixin import CharacterDisplayMixin
import pygame


class PlayerDisplayMixin(CharacterDisplayMixin):

    def _trigger_update(self, screen):
        return True

    def update_state(self, screen):
        super().update_state(screen)
        self.move_to_x_y_plane(screen)

    def blit(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        new_x = (width / 2 + width / 2 - self.current_animation.get_width()) / 2
        new_y = (height / 2 - self.current_animation.get_height() + height / 2) / 2
        screen.blit(self.current_animation, (new_x, new_y))

    def get_map_position(self, screen):
        player_map_x = (self.x + screen.get_width() / 2) / settings.SCALE_FACTOR / settings.TILE_WIDTH
        player_map_y = (self.y + screen.get_height() / 2) / settings.SCALE_FACTOR / settings.TILE_HEIGHT
        return player_map_x, player_map_y

    def move_to_x_y_plane(self, screen):
        animation_props = self.get_animation_props()
        directions = ["left", "right", "up", "down"]
        for direction in directions:
            if self.trig_movement_in_direction(screen, direction, animation_props):
                break
        else:
            if animation_props.get(self.direction):
                self.current_animation_frame = animation_props[self.direction]["stand_animation_frame"]
            self.direction = "stand_" + self.direction

    def trig_movement_in_direction(self, screen, direction, animation_props):
        if self.is_triggered_movement(screen,
                                      *animation_props[direction]["moved_pos"],
                                      self.get_needed_press_keys_props()[direction]
                                      ):
            self.change_direction(direction)
            self.x, self.y = animation_props[direction]["moved_pos"]
            return True
        return False

    @staticmethod
    def get_needed_press_keys_props():
        keys = pygame.key.get_pressed()
        return {
            "left": (keys[pygame.K_LEFT], keys[pygame.K_a]),
            "right": (keys[pygame.K_RIGHT], keys[pygame.K_d]),
            "up": (keys[pygame.K_UP], keys[pygame.K_w]),
            "down": (keys[pygame.K_DOWN], keys[pygame.K_s])
        }
