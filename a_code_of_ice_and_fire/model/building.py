from .position import Position


class Building(Position):

    def __init__(self, x, y, is_owned):
        super().__init__(x, y)
        self.is_owned = is_owned
