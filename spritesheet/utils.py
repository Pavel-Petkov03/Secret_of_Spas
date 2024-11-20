import json
import os
from spritesheet.spritesheet import SpriteSheet


def get_animation_matrix(name):
    json_file_path = os.path.join(os.path.dirname(__file__),  'spritesheets.json')
    with open(json_file_path, "r") as file:
        data = json.load(file)
        current_frame = data[name]
        filename = current_frame["filename"]
        rows = current_frame["rows"]
        cols = current_frame["cols"]
        row_max_cols = current_frame["row_max_cols"]
        instance = SpriteSheet(filename, rows, cols)
        matrix = instance.matrix
        for row_index in range(rows):
            matrix[row_index] = matrix[row_index][0:row_max_cols[row_index]]
        return matrix