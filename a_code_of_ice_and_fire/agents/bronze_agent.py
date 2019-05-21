import random
import sys
from typing import Callable

from ..model.cell import Cell
from ..model.environment import Environment
from ..actions.actions import Action, RandomWalkAction, MoveToUnownedCellAction, MoveToEnemyCellAction, KillEnemyAction, MoveToEnemyHQAction


class BronzeAgent:

  def spawn(self, environment: Environment):

    orders = []
    while True:
      if environment.gold <= 10:
        break

      level = 1 if environment.gold < 40 else 2

      start_cells_filter: Callable[[Cell], bool] = lambda cell: cell.is_owned

      start_cells = environment.map.get_all_cells(cell_filter=start_cells_filter)

      spawn_cell_filter: Callable[[Cell], bool] = lambda cell: (cell.unit is None) and \
                                                               (cell.building is None)

      free_owned_cells = environment.map.get_adjacent_cells(positions=start_cells, cell_filter=spawn_cell_filter)

      if not len(free_owned_cells):
        break

      spawn_cell = random.choice(free_owned_cells)

      orders.append(" ".join(["TRAIN", str(level), str(spawn_cell.x), str(spawn_cell.y)]))
      environment.gold -= level * 10

    return orders

  def act(self, environment: Environment):
    orders = []

    orders += self.spawn(environment)

    owned_units = environment.map.get_owned_units()

    actions: [Action] = [KillEnemyAction(),
                         MoveToEnemyCellAction(),
                         MoveToUnownedCellAction(),
                         MoveToEnemyHQAction(),
                         RandomWalkAction()]

    for unit in owned_units:
      for action in actions:
        order = action.try_execute(unit=unit, environment=environment)

        if order is not "":
          orders.append(order)
          break

    orders.append("WAIT")
    print(" ;".join(orders))
