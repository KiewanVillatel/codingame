from .position import Position
from enum import Enum


class BuildingType(Enum):
  HQ = 0
  Mine = 1
  Tower = 2


class Building(Position):

  def __init__(self, x, y, is_owned, type: BuildingType):
    super().__init__(x, y)
    self.is_owned = is_owned
    self.type = type
