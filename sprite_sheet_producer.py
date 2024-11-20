import pyglet.image


class SpriteSheetProducer:
    """
   s class is used to divide an image spreadsheet different images which will be used in the game
    :arg
        sheet_location:
            image location string
        rows:
            the max rows in the created grid
        cols:
            the max cols in the created grid


    """
    def __init__(self, sheet_location, rows, cols, *kwargs):
        self.rows = rows
        self.cols = cols
        self.sprite_sheet = pyglet.image.load(sheet_location)
        self.grid = self.__produce()
        self.kwargs = kwargs

    def __produce(self):
        grid = pyglet.image.ImageGrid(self.sprite_sheet,
                                      rows=self.rows,
                                      columns=self.cols,
                                      item_width=int(self.sprite_sheet.width / self.cols),
                                      item_height=int(self.sprite_sheet.height / self.rows),
                                      row_padding=0,
                                      column_padding=0
                                      )
        matrix = [grid[row * col + col] for col in range(self.cols) for row in range(self.rows)]
        return matrix

    def extract_animation_frame(self, row):
        return self.grid[row]

