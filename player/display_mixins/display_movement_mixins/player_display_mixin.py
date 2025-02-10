import settings
from errors import DeadError
from player.display_mixins.animation_frame_requester import MoveAnimationFrameRequester, \
    DiePlayerAnimationFrameRequester, PlayerAttackAnimationFrameRequester, DieEnemyAnimationFrameRequester
from player.display_mixins.display_movement_mixins.arrow_display_mixin import PlayerArrow
from player.display_mixins.display_movement_mixins.arrow_utils import init_arrow
from player.display_mixins.display_movement_mixins.base_display_character_mixin import CharacterDisplayMixin
import pygame


class PlayerDisplayMixin(CharacterDisplayMixin):
    def __init__(self, *args, **kwargs):
        CharacterDisplayMixin.__init__(self, *args, **kwargs)

    def _trigger_update(self, screen):
        return True

    def update_state(self, screen, delta_time, event_list, *args, **kwargs):
        self.move_to_x_y_plane(screen)

    def blit(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        current_animation = self.main_animation_frame_requester.current_animation
        new_x = (width - current_animation.get_width()) / 2
        new_y = (height - current_animation.get_height()) / 2
        screen.blit(current_animation, (new_x, new_y))

    def get_map_position(self, screen):
        tile_x = int(self.x // settings.TILE_WIDTH) + int(settings.VIEW_PORT_TILES_W // 2)
        tile_y = int(self.y // settings.TILE_WIDTH) + int(settings.VIEW_PORT_TILES_W // 2)
        return tile_x, tile_y

    def move_to_x_y_plane(self, screen):
        animation_props = self.get_animation_props()
        directions = ("left", "right", "up", "down")
        for direction in directions:
            if self.trig_movement_in_direction(screen, direction, animation_props):
                break
        else:
            self.handle_stand_animation(animation_props, directions)

    def handle_stand_animation(self, animation_props, directions):
        if animation_props.get(self.direction):
            self.main_animation_frame_requester.current_animation_frame = animation_props[self.direction][
                "stand_animation_frame"]
        if self.direction in directions:
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

    def move_to_block(self, screen, new_x, new_y):
        current_x = screen.get_width() / 2 / settings.SCALE_FACTOR / settings.TILE_WIDTH
        current_y = screen.get_height() / 2 / settings.SCALE_FACTOR / settings.TILE_HEIGHT
        player_map_x = int(current_x + new_x / settings.TILE_WIDTH)
        player_map_y = int(current_y + new_y / settings.TILE_HEIGHT)
        return self.collides_with_block(player_map_x, player_map_y)

    def die(self):
        self.main_animation_frame_requester = DiePlayerAnimationFrameRequester(self.animation_frames[9],
                                                                               20,
                                                                               5,
                                                                               is_repeated=False
                                                                               )

    def collides_with_snitch(self, screen):
        return self.find_tile_with_property(*self.get_map_position(screen), "is_snitch")

    def collides_with_gate(self, screen):
        return self.find_tile_with_property(*self.get_map_position(screen), "gate")


class PlayerAttackDisplayMixin(PlayerDisplayMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_state(self, screen, delta_time, event_list, *args, **kwargs):
        if kwargs["is_shooting_allowed"]:
            self.add_attacks(screen, event_list)
            if not isinstance(self.main_animation_frame_requester, PlayerAttackAnimationFrameRequester):
                super().update_state(screen, delta_time, event_list, *args, **kwargs)
        else:
            super().update_state(screen, delta_time, event_list, *args, **kwargs)

    def add_attacks(self, screen, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.attack_enemies(screen)
                if not isinstance(self.main_animation_frame_requester, PlayerAttackAnimationFrameRequester):
                    self.main_animation_frame_requester = PlayerAttackAnimationFrameRequester(
                        self.get_attack_props()[self.direction], 20, 5, is_repeated=False,
                        next_animation_request=self.move_animation_frame_requester
                    )
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.dungeon_data.player.arrows.append(
                    init_arrow(1000, self.dungeon_data, self.dungeon_data.player, PlayerArrow)
                )

    def attack_enemies(self, screen):
        x, y = self.get_map_position(screen)
        dir_dict = {
            "left": (x - 1, y),
            "right": (x + 1, y),
            "up": (x, y - 1),
            "down": (x, y + 1),
            "stand_left": (x - 1, y),
            "stand_right": (x + 1, y),
            "stand_up": (x, y - 1),
            "stand_down": (x, y + 1)
        }
        for enemy in self.dungeon_data.enemies:
            if enemy.get_map_position(screen) == dir_dict[self.direction] or enemy.get_map_position(
                    screen) == self.get_map_position(screen):
                try:
                    enemy.health -= self.dungeon_data.player.damage
                except DeadError:
                    if not isinstance(enemy.main_animation_frame_requester, DieEnemyAnimationFrameRequester):
                        enemy.main_animation_frame_requester = DieEnemyAnimationFrameRequester(
                            enemy.animation_frames[9],
                            20,
                            5,
                            is_repeated=False,
                            to_remove=enemy
                        )

    def get_attack_props(self):
        return {
            "left": self.animation_frames[12],
            "right": self.animation_frames[7],
            "up": self.animation_frames[8],
            "down": self.animation_frames[6],
            "stand_left": self.animation_frames[12],
            "stand_right": self.animation_frames[7],
            "stand_up": self.animation_frames[8],
            "stand_down": self.animation_frames[6],
        }
