from .cell import Cell
from ..model.position import Position
from ..model.unit import Unit
from typing import Callable


class Map:
  map_size = 12

  def __init__(self):
    self._grid = [[Cell(x=i, y=j) for i in range(Map.map_size)] for j in range(Map.map_size)]

  def update_cell(self, cell: Cell):
    self._grid[cell.y][cell.x] = cell

  def get_cell(self, x, y):
    return self._grid[y][x]

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
