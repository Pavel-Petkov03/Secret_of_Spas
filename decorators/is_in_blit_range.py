import settings


class IsInBlitRange:
    def __init__(self, func):
        self.func = func

    def __call__(self, instance, x, y, screen, image):
        if self.is_in_x_range(instance, x) and self.is_in_y_range(instance, y):
            return self.func(instance, x, y, screen, image)

    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            return self(instance, *args, **kwargs)

        return wrapper

    @staticmethod
    def is_in_x_range(instance, x):
        left_bond = instance.player.x - settings.TILE_WIDTH
        right_bond = instance.player.x + settings.VIEW_PORT_TILES_W * settings.TILE_WIDTH + settings.TILE_WIDTH
        return left_bond <= x <= right_bond

    @staticmethod
    def is_in_y_range(instance, y):
        left_bond = instance.player.y - settings.TILE_HEIGHT
        right_bond = instance.player.y + settings.VIEW_PORT_TILES_H * settings.TILE_HEIGHT + settings.TILE_HEIGHT
        return left_bond <= y <= right_bond
