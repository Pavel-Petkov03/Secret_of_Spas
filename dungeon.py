class GameMap:
    attack_enabled = False

    def __init__(self, name, texture_matrix, game_matrix):
        self.name = name
        self.texture_matrix = texture_matrix
        self.game_matrix = game_matrix

    def get_map_window(self):
        pass


class Village(GameMap):
    attack_enabled = False


class Dungeon(GameMap):
    attack_enabled = True

    def __init__(self, name, texture_matrix, game_matrix):
        super().__init__(name, texture_matrix, game_matrix)
        self.enemies = []

    def clear(self):
        pass

    def populate(self):
        pass
