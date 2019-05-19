from .position import Position


class Cell(Position):

    def __init__(self, x, y):
        super().__init__(x, y)

        self.is_void = None
        self.is_owned = None
        self.is_active = None

        self.unit = None
