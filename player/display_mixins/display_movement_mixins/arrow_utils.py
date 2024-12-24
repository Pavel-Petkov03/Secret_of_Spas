import pygame
from spritesheet.utils import get_animation_matrix


def init_arrow(damage, dungeon_data, executor, arrow_class):
    player = executor
    arrow_matrix = get_animation_matrix("arrow_projectile")
    arrow_matrix[0].extend(arrow_matrix[1])
    result = [arrow_matrix[0]]
    degrees_rotate = [90, 180, 270]
    for i in range(3):
        current_degrees = degrees_rotate[i]
        arr = []
        for col in range(len(result)):
            current_image = result[0][col]
            rotated_image = pygame.transform.rotate(current_image, current_degrees)
            arr.append(rotated_image)
        result.append(arr)

    dir_dict = {
        "down": 0,
        "right": 1,
        "up": 2,
        "left": 3,
        "stand_down": 0,
        "stand_right": 1,
        "stand_up": 2,
        "stand_left": 3,
    }
    return arrow_class(executor, damage,
                       player.direction,
                       player.x,
                       player.y,
                       result[dir_dict[player.direction]],
                       result,
                       dungeon_data
                       )
