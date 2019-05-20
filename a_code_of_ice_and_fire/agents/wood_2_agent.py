import random
import sys
from typing import Callable

from ..model.cell import Cell
from ..model.environment import Environment


class Wood2Agent:

  def spawn(self, environment: Environment):

    orders = []
    while True:
      if environment.gold <= 10:
        break

      level = 1

      start_cells_filter: Callable[[Cell], bool] = lambda cell: cell.is_owned

      start_cells = environment.map.get_all_cells(cell_filter=start_cells_filter)

      spawn_cell_filter: Callable[[Cell], bool] = lambda cell: (cell.unit is None) and \
                                                               (cell.building is None)

      free_owned_cells = environment.map.get_adjacent_cells(positions=start_cells, cell_filter=spawn_cell_filter)

      if not len(free_owned_cells):
        break

      spawn_cell = random.choice(free_owned_cells)

      orders.append(" ".join(["TRAIN", str(level), str(spawn_cell.x), str(spawn_cell.y)]))
      environment.gold -= 10

    return orders

  def act(self, environment: Environment):
    orders = []

    orders += self.spawn(environment)

    owned_units = environment.map.get_owned_units()

    for unit in owned_units:
      adjacent_cells = environment.map.get_adjacent_cells([unit])

      if len(adjacent_cells):
        target_cell = random.choice(adjacent_cells)
        orders.append(" ".join(["MOVE", str(unit.id), str(target_cell.x), str(target_cell.y)]))

    orders.append("WAIT")
    print(" ;".join(orders))
