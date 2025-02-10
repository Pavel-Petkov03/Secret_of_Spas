class DeadError(Exception):
    def __init__(self, message, character):
        super().__init__(message)
        self.character = character


class RemoveEnemyFromScreenError(Exception):
    def __init__(self, message, enemy):
        super().__init__(message)
        self.enemy = enemy
