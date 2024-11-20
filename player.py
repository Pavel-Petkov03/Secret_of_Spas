from collections import deque
from abc import ABC, abstractmethod


class DeadError(Exception):
    pass


MAIN_CHARACTER_GAME_MATRIX_REPRESENT = "K"
EMPTY_FIELD = " "


class Player(ABC):
    """

    """

    def __init__(self, name, health_points, attack, level=1,
                 current_dungeon=None,
                 current_animation_frame=None,
                 animation_frames=None,
                 pos=None,

                 ):
        self.__name = name
        self.attack = attack
        self.__health_points = health_points
        self.current_animation_frame = current_animation_frame
        self.animation_frames = animation_frames
        self.x = pos[0]
        self.y = pos[1]
        self.level = level
        self.current_dungeon = current_dungeon
        self.path_to_target = None

    @property
    def name(self):
        return self.__name

    @property
    def health_points(self):
        return self.__health_points

    @health_points.setter
    def health_points(self, value):
        if self.__health_points - value < 0:
            raise DeadError("You are dead")
        self.__health_points -= value

    def change_animation_frame(self, new_frame_name):
        """
        :param new_frame_name: string name of frame which is in animation_frames dict
        """
        self.current_animation_frame = self.animation_frames[new_frame_name]

    def __recurse_detect_target(self):
        game_matrix = self.current_dungeon.game_matrix
        stack = [(self.x, self.y, [])]
        visited = [[False for _ in range(len(game_matrix[0]))] for _ in range(len(game_matrix))]
        while stack:
            x, y, path = stack.pop()
            if x < 0 or y < 0 or x >= len(game_matrix) or y >= len(game_matrix[0]) or visited[x][y]:
                continue
            visited[x][y] = True
            new_path = deque(path + [(x, y)])
            if game_matrix[x][y] == MAIN_CHARACTER_GAME_MATRIX_REPRESENT:
                return new_path
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                stack.append((x + dx, y + dy, new_path))

        return None

    @abstractmethod
    def move(self):
        pass


class MainPlayer(Player):
    MAX_MAIN_PLAYER_POINTS = 100

    def __init__(self, name, health):
        super().__init__("Kuncho", 15, health)
        self.inventory = []

    def regenerate(self, health_points):
        self.health_points += health_points
        if self.health_points > MainPlayer.MAX_MAIN_PLAYER_POINTS:
            self.health_points = MainPlayer.MAX_MAIN_PLAYER_POINTS

    def move_player(self, x, y):
        pass



class Enemy(Player, ABC):
    def __init__(self, name, health, attack, **kwargs):
        super(Enemy, self).__init__(name, health, attack, **kwargs)
        self.path_to_target = deque()
        self.current_dungeon = None

    def move(self):
        path = self.detect_target()
        if path:
            self.x, self.y = path.popleft()

    def _in_range(self):
        pass

    def detect_target(self):
        if self._in_range():
            self.path_to_target = self.__recurse_detect_target()
        return deque()

    def attack(self):
        player = self.current_dungeon.player


class Archer(Enemy):
    """
    I think something like if we click right mouse button
    if we move we will stop and shoot with bow
    else we just shoot
    """

    def __init__(self, name, health_points, **kwargs):
        super().__init__(name, health_points, **kwargs)

    def move(self):
        pass


class Infantry(Enemy):
    """
    I think something like if we click left mouse button
    the player to go to the enemy if an enemy is clicked and when it is in proper range
    to hit with the primary attack
    """

    def move(self):
        pass
        # трябва да измисля логика, която по координатите на мишката разбира на къде да тръгне в game matricata
