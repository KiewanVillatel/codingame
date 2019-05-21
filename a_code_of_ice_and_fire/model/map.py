from .cell import Cell
from ..model.position import Position
from ..model.unit import Unit
from typing import Callable
from ..model.building import BuildingType


class Map:
  map_size = 12

  def __init__(self):
    self._grid = [[Cell(x=i, y=j) for i in range(Map.map_size)] for j in range(Map.map_size)]

  def get_cell(self, x, y):
    return self._grid[y][x]

  def get_cell_from_pos(self, pos: Position):
    return self.get_cell(pos.x, pos.y)

  def is_in_grid(self, x, y):
    return 0 <= x < Map.map_size and 0 <= y < Map.map_size

  def get_adjacent_cells(self, positions: [Position], cell_filter: Callable[[Cell], bool] = None) -> [Cell]:
    cells = [self.get_cell(x, y) for pos in positions for x, y in
             [(pos.x - 1, pos.y), (pos.x + 1, pos.y), (pos.x, pos.y - 1), (pos.x, pos.y + 1)] if
             self.is_in_grid(x, y)]

    if cell_filter is not None:
      cells = list(filter(cell_filter, cells))
    return cells

  def get_owned_units(self) -> [Unit]:
    return [cell.unit for line in self._grid for cell in line if cell.unit is not None and cell.unit.is_owned]

  def get_all_cells(self, cell_filter: Callable[[Cell], bool] = None) -> [Cell]:
    cells = [cell for line in self._grid for cell in line]
    if cell_filter is not None:
      cells = list(filter(cell_filter, cells))
    return cells

  def get_owned_mines(self):
    cell_filter: Callable[[Cell], bool] = lambda cell: cell.building is not None and \
                                                       cell.building.is_owned and \
                                                       cell.building.type is BuildingType.Mine

    return self.get_all_cells(cell_filter=cell_filter)

  def get_HQ_cell(self) -> Cell:
    if self.get_cell(0, 0).is_owned:
      return self.get_cell(0, 0)
    else:
      return self.get_cell(11, 11)

  def get_opponent_HQ_cell(self) -> Cell:
    if not self.get_cell(0, 0).is_owned:
      return self.get_cell(0, 0)
    else:
      return self.get_cell(11, 11)

