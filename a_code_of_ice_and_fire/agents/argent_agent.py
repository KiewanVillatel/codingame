import random
import sys
from typing import Callable

from ..global_vars import BUILD_TOWER_MIN_UNITS, BUILD_TOWER_MIN_GOLD, SPAWN_LVL_2_MIN_GOLD
from ..global_vars import SPAWN_LVL_3_MIN_GOLD, SPAWN_LVL_3_MIN_UNITS, SPAWN_LVL_2_MIN_UNITS
from ..model.building import Building, BuildingType
from ..model.cell import Cell
from ..model.environment import Environment
from ..actions.actions import Action, RandomWalkAction, MoveToUnownedCellAction, MoveToEnemyCellAction, KillEnemyAction
from ..actions.actions import MoveToEnemyHQAction
from ..model.unit import Unit


class ArgentAgent:

  def build_towers(self, environment: Environment) -> [str]:
    hq_cell = environment.map.get_HQ_cell()
    candidate_cells = environment.map.get_adjacent_cells([hq_cell])

    orders = []

    if len(environment.map.get_owned_units()) < BUILD_TOWER_MIN_UNITS:
      return orders

    for cell in candidate_cells:
      if environment.gold < BUILD_TOWER_MIN_GOLD:
        return orders
      if cell.building is None and cell.is_owned and cell.unit is None:
        environment.gold -= 15
        cell.building = Building(cell.x, cell.y, is_owned=True, type=BuildingType.Tower)
        orders.append("BUILD TOWER {} {}".format(cell.x, cell.y))

    return orders

  def build_mines(self, environment: Environment) -> [str]:
    orders = []

    owned_mines = environment.map.get_owned_mines()

    mine_spot_filter: Callable[[Cell], bool] = lambda cell: cell.is_owned and \
                                                            cell.is_active and \
                                                            cell.is_mine_spot and \
                                                            cell.building is None and \
                                                            cell.unit is None

    mine_spots = environment.map.get_all_cells(cell_filter=mine_spot_filter)

    nb_mines = len(owned_mines)

    for mine_spot in mine_spots:
      mine_price = 20 + 4 * nb_mines

      if mine_price > environment.gold:
        return orders

      orders.append("BUILD MINE " + str(mine_spot.x) + " " + str(mine_spot.y))

      environment.gold -= mine_price
      mine_spot.building = Building(mine_spot.x, mine_spot.y, is_owned=True, type=BuildingType.Mine)

    return orders

  def spawn(self, environment: Environment):

    orders = []
    while True:
      if environment.gold <= 10:
        break

      level = 1

      if environment.gold >= SPAWN_LVL_3_MIN_GOLD and len(environment.map.get_owned_units()) >= SPAWN_LVL_3_MIN_UNITS:
        level = 3
      elif environment.gold >= SPAWN_LVL_2_MIN_GOLD and len(environment.map.get_owned_units()) >= SPAWN_LVL_2_MIN_UNITS:
        level = 2

      start_cells_filter: Callable[[Cell], bool] = lambda cell: cell.is_owned

      start_cells = environment.map.get_all_cells(cell_filter=start_cells_filter)

      base_spawn_filter: Callable[[Cell], bool] = lambda cell: (
                                                              cell.unit is None or cell.unit.level < level or level == 3) and \
                                                               cell.building is None and \
                                                               not cell.is_void

      spawn_cell_filter: Callable[[Cell], bool] = lambda cell: (base_spawn_filter(cell) and cell.is_owned is False)

      candidate_cells = environment.map.get_adjacent_cells(positions=start_cells, cell_filter=spawn_cell_filter)

      # If no candidate neutral or opponent cells, try on owned cells
      if not len(candidate_cells):
        candidate_cells = environment.map.get_adjacent_cells(positions=start_cells, cell_filter=base_spawn_filter)

      if not len(candidate_cells):
        break

      opponent_hq = environment.map.get_opponent_HQ_cell()

      candidate_cells.sort(key=lambda c: (c.x-opponent_hq.x)**2+(c.y-opponent_hq.y)**2)

      spawn_cell = candidate_cells[0]
      spawn_cell.is_owned = True
      spawn_cell.unit = Unit(spawn_cell.x, spawn_cell.y, -1, is_owned=True, level=level)
      orders.append(" ".join(["TRAIN", str(level), str(spawn_cell.x), str(spawn_cell.y)]))
      environment.gold -= level * 10

    return orders

  def act(self, environment: Environment):
    orders = []

    orders += self.build_mines(environment)
    orders += self.build_towers(environment)
    orders += self.spawn(environment)

    owned_units = environment.map.get_owned_units()

    actions: [Action] = [KillEnemyAction(),
                         MoveToEnemyCellAction(),
                         MoveToUnownedCellAction(),
                         MoveToEnemyHQAction(),
                         RandomWalkAction()]

    for unit in owned_units:
      # An unit with an id of -1 has just been created and can't receive orders
      if unit.id is -1:
        continue
      for action in actions:
        order = action.try_execute(unit=unit, environment=environment)

        if order is not "":
          orders.append(order)
          break

    orders.append("WAIT")
    print(" ;".join(orders))
