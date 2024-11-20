import pyglet
from pyglet.window import key
# Constants
TILE_SIZE = 16
MAP_WIDTH, MAP_HEIGHT = 100, 100
VISIBLE_WIDTH, VISIBLE_HEIGHT = 40, 30


class GameWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(VISIBLE_WIDTH * TILE_SIZE, VISIBLE_HEIGHT * TILE_SIZE)

        self.tile_image = pyglet.image.load('src/tiles/Path_Middle.png')
        self.batch = pyglet.graphics.Batch()
        self.tiles = []
        self.set_location(200, 60)  # hardcoded
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                sprite = pyglet.sprite.Sprite(self.tile_image, x * TILE_SIZE, y * TILE_SIZE, batch=self.batch)
                self.tiles.append(sprite)

    def on_draw(self):
        self.clear()
        self.batch.draw()


if __name__ == "__main__":
    window = GameWindow()
    pyglet.app.run()
