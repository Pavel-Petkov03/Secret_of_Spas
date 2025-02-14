from spritesheet.utils import get_animation_matrix
from vehicle.car_display import Car

CAR_X = 1200
CAR_Y = 400


def get_car(dungeon_data):
    animation_frames = get_animation_matrix("car_movement")
    car_frames = [
        [animation_frames[0][1]],
        [animation_frames[0][3]],
        [animation_frames[0][5]],
        [animation_frames[0][7]],
    ]
    return Car(CAR_X, CAR_Y, car_frames[0], car_frames, dungeon_data)
