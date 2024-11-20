class DeadError(Exception):
    pass


class Player:
    def __init__(self, name, health, x, y, damage, current_animation_frame=None, animations_frames=None):
        self._name = name
        self._health = health
        self._x = x
        self._y = y
        self._damage = damage
        self._current_animation_frame = current_animation_frame
        self._animation_frames = animations_frames

    @property
    def current_animation_frame(self):
        return self._current_animation_frame

    @current_animation_frame.setter
    def current_animation_frame(self, value):
        if value not in self._animation_frames.values():
            raise ValueError("Not valid animation frame")
        self._current_animation_frame = value

    @property
    def animation_frames(self):
        return self._animation_frames.copy()

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if self.health - value <= 0:
            raise DeadError("You are dead")
        self._health -= value
