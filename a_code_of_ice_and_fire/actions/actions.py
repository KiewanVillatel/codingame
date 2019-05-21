import sys
from abc import abstractmethod
from typing import Callable

from ..model.cell import Cell
from ..model.environment import Environment
from ..model.unit import Unit

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
    cell_filter: Callable[[Cell], bool] = lambda cell: not cell.is_void

    adjacent_cells = environment.map.get_adjacent_cells([unit], cell_filter=cell_filter)

    if len(adjacent_cells):
      target_cell = random.choice(adjacent_cells)
      return " ".join(["MOVE", str(unit.id), str(target_cell.x), str(target_cell.y)])

    return ""


class MoveToUnownedCellAction(Action):

  def get_name(self):
    return "MoveToUnownedCellAction"

  def try_execute(self, unit: Unit, environment: Environment) -> str:
    cell_filter: Callable[[Cell], bool] = lambda cell: not (cell.is_void or cell.is_owned)

    adjacent_cells = environment.map.get_adjacent_cells([unit], cell_filter=cell_filter)

    if len(adjacent_cells):
      target_cell = random.choice(adjacent_cells)
      print(target_cell.is_owned, file=sys.stderr)
      return " ".join(["MOVE", str(unit.id), str(target_cell.x), str(target_cell.y)])

    return ""


class MoveToEnemyCellAction(Action):

  def get_name(self):
    return "MoveToEnemyCellAction"

  def try_execute(self, unit: Unit, environment: Environment) -> str:
    cell_filter: Callable[[Cell], bool] = lambda cell: not (cell.is_void or cell.is_neutral or cell.is_owned)

    adjacent_cells = environment.map.get_adjacent_cells([unit], cell_filter=cell_filter)

    if len(adjacent_cells):
      target_cell = random.choice(adjacent_cells)
      print(target_cell.is_owned, file=sys.stderr)
      return " ".join(["MOVE", str(unit.id), str(target_cell.x), str(target_cell.y)])

    return ""


class KillEnemyAction(Action):

  def get_name(self):
    return "KillEnemyAction"

  def try_execute(self, unit: Unit, environment: Environment) -> str:
    cell_filter: Callable[[Cell], bool] = lambda cell: not (cell.is_void or cell.is_neutral or cell.is_owned) \
                                                       and (cell.unit is not None) \
                                                       and (cell.unit.level < unit.level)

    adjacent_cells = environment.map.get_adjacent_cells([unit], cell_filter=cell_filter)

    if len(adjacent_cells):
      target_cell = random.choice(adjacent_cells)
      print(target_cell.is_owned, file=sys.stderr)
      return " ".join(["MOVE", str(unit.id), str(target_cell.x), str(target_cell.y)])

    return ""


class MoveToEnemyHQAction(Action):

  def get_name(self):
    return "MoveToEnemyHQAction"

  def try_execute(self, unit: Unit, environment: Environment) -> str:
    return " ".join(["MOVE", str(unit.id), str(11), str(11)])
