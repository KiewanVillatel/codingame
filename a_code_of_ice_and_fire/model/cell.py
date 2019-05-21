from .position import Position
from .building import Building


class Cell(Position):

  def __init__(self, x, y):
    super().__init__(x, y)

    self.is_void = None
    self.is_owned = None
    self.is_active = None
    self.is_neutral = None
    self.is_mine_spot = False

    self.unit = None
    self.building: Building = None
