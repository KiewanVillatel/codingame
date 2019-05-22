import sys
from abc import abstractmethod
from typing import Callable

from ..model.cell import Cell
from ..model.environment import Environment
from ..model.unit import Unit
from ..model.building import BuildingType

import random


class Action:

  @abstractmethod
  def get_name(self):
    pass

  @abstractmethod
  def try_execute(self, unit: Unit, environment: Environment) -> bool:
    pass


class RandomWalkAction(Action):

  def get_name(self):
    return "RandomWalkAction"

  def try_execute(self, unit: Unit, environment: Environment) -> str:
    cell_filter: Callable[[Cell], bool] = lambda cell: (not cell.is_void) and \
                                                       (cell.unit is None or (not cell.unit.is_owned and (
                                                             unit.level > cell.unit.level or unit.level == 3)))

    adjacent_cells = environment.map.get_adjacent_cells([unit], cell_filter=cell_filter)

    if len(adjacent_cells):
      target_cell = random.choice(adjacent_cells)
      return environment.map.move_unit(unit, target_cell)

    return ""


class MoveToUnownedCellAction(Action):

  def get_name(self):
    return "MoveToUnownedCellAction"

  def try_execute(self, unit: Unit, environment: Environment) -> str:
    cell_filter: Callable[[Cell], bool] = lambda cell: not (cell.is_void or cell.is_owned) and \
                                                       (cell.unit is None or (not cell.unit.is_owned and (
                                                             unit.level > cell.unit.level or unit.level == 3)))

    adjacent_cells = environment.map.get_adjacent_cells([unit], cell_filter=cell_filter)

    if len(adjacent_cells):
      target_cell = random.choice(adjacent_cells)
      return environment.map.move_unit(unit, target_cell)

    return ""


class MoveToEnemyCellAction(Action):

  def get_name(self):
    return "MoveToEnemyCellAction"

  def try_execute(self, unit: Unit, environment: Environment) -> str:
    cell_filter: Callable[[Cell], bool] = lambda cell: not (cell.is_void or cell.is_neutral or cell.is_owned) and \
                                                       (cell.unit is None or (not cell.unit.is_owned and (
                                                             unit.level > cell.unit.level or unit.level == 3)))

    adjacent_cells = environment.map.get_adjacent_cells([unit], cell_filter=cell_filter)

    if len(adjacent_cells):
      target_cell = random.choice(adjacent_cells)
      return environment.map.move_unit(unit, target_cell)

    return ""


class KillEnemyAction(Action):

  def get_name(self):
    return "KillEnemyAction"

  def try_execute(self, unit: Unit, environment: Environment) -> str:
    cell_filter: Callable[[Cell], bool] = lambda cell: not (cell.is_void or cell.is_neutral or cell.is_owned) \
                                                       and (cell.unit is not None) \
                                                       and ((cell.unit.level < unit.level) or unit.level == 3)

    adjacent_cells = environment.map.get_adjacent_cells([unit], cell_filter=cell_filter)

    if len(adjacent_cells):
      target_cell = random.choice(adjacent_cells)
      return environment.map.move_unit(unit, target_cell)

    return ""


class MoveToEnemyHQAction(Action):

  def get_name(self):
    return "MoveToEnemyHQAction"

  def try_execute(self, unit: Unit, environment: Environment) -> str:
    target_cell = environment.map.get_opponent_HQ_cell()

    return " ".join(["MOVE", str(unit.id), str(target_cell.x), str(target_cell.y)])


class DestroyBuildingAction(Action):

  def get_name(self):
    return "DestroyBuildingAction"

  def try_execute(self, unit: Unit, environment: Environment) -> str:
    cell_filter: Callable[[Cell], bool] = lambda c: c.building is not None and \
                                                    c.is_owned is False and (c.building.type is not BuildingType.Tower or unit.level == 3)

    candidate_cells = environment.map.get_adjacent_cells([unit], cell_filter=cell_filter)

    if len(candidate_cells) == 0:
      return ""

    return environment.map.move_unit(unit, candidate_cells[0])
