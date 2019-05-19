from ..model.position import Position
from .cell import Cell
from ..model.unit import Unit

class Map:
    map_size = 12

    def __init__(self):
        self._grid = [[Cell(x=i, y=j) for j in range(Map.map_size)] for i in range(Map.map_size)]

    def update_cell(self, cell: Cell):
        self._grid[cell.x][cell.y] = cell

    def is_in_grid(self, x, y):
        return 0 <= x < Map.map_size and 0 <= y < Map.map_size

    def get_adjacent_cells(self, pos: Position):
        return [
            (self._grid[x][y] for x, y in [(pos.x - 1, pos.y), (pos.x + 1, pos.y), (pos.x, pos.y - 1), (pos.x, pos.y + 1)] if self.is_in_grid(x, y))]

    def get_owned_units(self) -> [Unit]:
        return [cell.unit for line in self._grid for cell in line if cell.unit is not None and cell.unit.is_owned]
