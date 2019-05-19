from .position import Position


class Unit(Position):

    def __init__(self, x, y, unit_id, is_owned, level):
        super().__init__(x, y)

        self.id = unit_id
        self.is_owned = is_owned
        self.level = level
