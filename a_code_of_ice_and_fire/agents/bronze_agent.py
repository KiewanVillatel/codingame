import random
import sys
from typing import Callable

from ..model.building import Building, BuildingType
from ..model.cell import Cell
from ..model.environment import Environment
from ..actions.actions import Action, RandomWalkAction, MoveToUnownedCellAction, MoveToEnemyCellAction, KillEnemyAction
from ..actions.actions import MoveToEnemyHQAction


class BronzeAgent:

  def build_mines(self, environment: Environment) -> [str]:
    owned_mines = environment.map.get_owned_mines()

    mine_spot_filter: Callable[[Cell], bool] = lambda cell: cell.is_owned and \
                                                            cell.is_active and \
                                                            cell.is_mine_spot and \
                                                            cell.building is None and \
                                                            cell.unit is None

    mine_spots = environment.map.get_all_cells(cell_filter=mine_spot_filter)

    print(len(mine_spots), file=sys.stderr)

    nb_mines = len(owned_mines)

    orders = []

    for mine_spot in mine_spots:
      mine_price = 20 + 4 * nb_mines

      if mine_price > environment.gold:
        return orders

      # orders.append("BUILD MINE ".format(mine_spot.x, mine_spot.y))
      orders.append("BUILD MINE " + str(mine_spot.x) + " " + str(mine_spot.y))

      environment.gold -= mine_price
      mine_spot.building = Building(mine_spot.x, mine_spot.y, is_owned=True, type=BuildingType.Mine)

    return orders

  def spawn(self, environment: Environment):

    orders = []
    while True:
      if environment.gold <= 10:
        break

      level = 1 if environment.gold < 40 else 2

      start_cells_filter: Callable[[Cell], bool] = lambda cell: cell.is_owned

      start_cells = environment.map.get_all_cells(cell_filter=start_cells_filter)

      spawn_cell_filter: Callable[[Cell], bool] = lambda cell: (cell.unit is None or cell.unit.level < level or level == 3) and \
                                                               (cell.building is None) and \
                                                               cell.is_owned is False

      free_owned_cells = environment.map.get_adjacent_cells(positions=start_cells, cell_filter=spawn_cell_filter)

      if not len(free_owned_cells):
        break

      spawn_cell = random.choice(free_owned_cells)

      orders.append(" ".join(["TRAIN", str(level), str(spawn_cell.x), str(spawn_cell.y)]))
      environment.gold -= level * 10

    return orders

  def act(self, environment: Environment):
    orders = []

    orders += self.build_mines(environment)

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
