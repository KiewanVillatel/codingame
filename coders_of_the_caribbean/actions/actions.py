import random
import sys

from coders_of_the_caribbean.global_vars import ship_last_barrels, ship_last_shots, ships_target_pos, targeted_ships
from coders_of_the_caribbean.model.model import Pos, Ship, Mine, Barrel


def iround(x):
  """iround(number) -> integer
  Round a number to the nearest integer."""
  return int(round(x) - .5) + (x > 0)


class Action:
  def try_execute(self, grid, turn, ship):
    pass


class MoveAction(Action):
  def __init__(self, pos):
    self.pos = pos

  def try_execute(self, grid, turn, ship):
    ships_target_pos[ship.id] = self.pos
    print('MOVE ' + self.pos.to_oddr_string())
    return True


class MoveToNearestBarrelAction(Action):
  def __init__(self, max_ship_rum=100):
    self._max_ship_rum = max_ship_rum

  def try_execute(self, grid, turn, ship):
    if ship.rum > self._max_ship_rum:
      return False
    if ship.id not in ship_last_barrels or not isinstance(grid.get(ship_last_barrels[ship.id].pos), Barrel):
      nearest_barrel = grid.find_nearest(Barrel, ship.pos, lambda b: b not in ship_last_barrels)
      if nearest_barrel is None:
        return False
      ship_last_barrels[ship.id] = nearest_barrel
    MoveAction(ship_last_barrels[ship.id].pos).try_execute(grid, turn, ship)
    return True


class MoveToTargetedShip(Action):
  def __init__(self, min_ship_rum=0):
    self._min_ship_rum = min_ship_rum

  def try_execute(self, grid, turn, ship):
    if ship.rum < self._min_ship_rum:
      return False
    if len(targeted_ships) > 0:
      return MoveAction(targeted_ships[0].pos).try_execute(grid, turn, ship)
    return False


class MoveToNearestEnemyAction(Action):
  def __init__(self):
    self.previous_target_enemy = None

  def try_execute(self, grid, turn, ship):
    if self.previous_target_enemy == None or not isinstance(grid.get(self.previous_target_enemy.pos), Ship):
      self.previous_target_enemy = grid.find_nearest(Ship, ship.pos, lambda s: not s.owner)
    if self.previous_target_enemy == None:
      return False
    return MoveAction(self.previous_target_enemy.pos).try_execute(grid, turn, ship)


class RandomMove(Action):
  def try_execute(self, grid, turn, ship):
    return MoveAction(Pos.from_oddr(random.randint(0, 19), random.randint(0, 19))).try_execute(grid, turn, ship)


class FireAction(Action):
  def __init__(self, target):
    self._target = target

  def try_execute(self, grid, turn, ship):
    if ship.id in ship_last_shots and turn - ship_last_shots[ship.id] <= 2:
      return False

    if not grid.in_grid(self._target.pos):
      return False

    ship_last_shots[ship.id] = turn
    print('FIRE ' + self._target.pos.to_oddr_string())
    return True


class FireTargetAction(Action):
  def __init__(self, target):
    self._ship_target = target
    self.target = None

  def try_execute(self, grid, turn, ship):
    if self._ship_target is None:
      return False

    if ship.id in ship_last_shots and turn - ship_last_shots[ship.id] <= 2:
      return False

    if not isinstance(grid.get(self._ship_target.pos), Ship):
      return False

    for i in range(3):
      target_x = self._ship_target.pos.x + (i + 1) * self._ship_target.speed * self._ship_target.rotation.x
      target_y = self._ship_target.pos.y + (i + 1) * self._ship_target.speed * self._ship_target.rotation.y
      target_z = self._ship_target.pos.z + (i + 1) * self._ship_target.speed * self._ship_target.rotation.z
      target_pos = Pos(target_x, target_y, target_z)
      t_shot = 1 + iround(target_pos.dist_to(ship.front_pos()) / 3)
      if t_shot - i < 2 and grid.in_grid(target_pos):
        self.target = grid.get(target_pos)
        break

    if self.target is None:
      return False

    if ship.front_pos().dist_to(self.target.pos) > 10:
      return False

    print('shot', self._ship_target.pos.to_string(), self._ship_target.rotation.to_string(),
          self.target.pos.to_string(), file=sys.stderr)
    targeted_ships.append(self._ship_target)
    return FireAction(self.target).try_execute(grid, turn, ship)


class ShotNearestEnemyAction(Action):
  def try_execute(self, grid, turn, ship):
    target = grid.find_nearest(Ship, ship.pos, lambda s: not s.owner)

    return FireTargetAction(target).try_execute(grid, turn, ship)


class ShotMineAction(Action):
  def try_execute(self, grid, turn, ship):
    target = grid.find_nearest(Mine, ship.pos,
                               lambda m: ship.rotation.x * (m.pos.x - ship.pos.x) >= 0 and ship.rotation.y * (
                                 m.pos.y - ship.pos.y) >= 0 and ship.rotation.z * (
                                 m.pos.z - ship.pos.z) >= 0)

    if target == None:
      return False

    if target.pos.dist_to(ship.front_pos()) > 5:
      return False

    return FireAction(target).try_execute(grid, turn, ship)


class ShotTargetedEnemyAction(Action):
  def __init__(self):
    self.fire_action = None

  def try_execute(self, grid, turn, ship):
    for targeted_ship in targeted_ships:
      fire_action = FireTargetAction(targeted_ship)
      if fire_action.try_execute(grid, turn, ship):
        return True
    return False


class Accelerate(Action):
  def try_execute(self, grid, turn, ship):
    # if turn - self._last_accelerate <= 3:
    #   return False
    if ship.speed == 2:
      return False
    if ship.id not in ships_target_pos:
      return False
    target_pos = ships_target_pos[ship.id]
    if not target_pos.is_in_direction(ship.pos, ship.rotation):
      return False
    print('FASTER')
    return True


class SlowerAction(Action):
  def try_execute(self, grid, turn, ship):
    if ship.speed == 0:
      return False
    print('SLOWER')
    return True


class StopIfMine(Action):
  def try_execute(self, grid, turn, ship):
    if ship.speed == 0:
      return False
    cells_pos_in_front = ship.get_pos_in_line()
    for cell_pos in cells_pos_in_front:
      if grid.in_grid(cell_pos) and isinstance(grid.get(cell_pos), Mine):
        return SlowerAction().try_execute(grid, turn, ship)
    return False


class PlaceMineAction(Action):
  def __init__(self):
    self.last_mine = -99999

  def try_execute(self, grid, turn, ship):
    if turn - self.last_mine <= 5:
      return False
    self.last_mine = turn
    print('MINE')
    return True


class AvoidCannonballAction(Action):
  def try_execute(self, grid, turn, ship):
    action_map = {
      ship.get_next_pos(): [Accelerate(), SlowerAction()],
      ship.get_next_front_pos(): [SlowerAction()],
      ship.get_next_back_pos(): [Accelerate()]
    }

    for pos, actions in action_map.items():
      if not grid.in_grid(pos):
        continue
      next_cell = grid.get(pos)
      cannonball = next_cell.cannonball
      if cannonball is not None and cannonball._time_before_impact == 1:
        for action in actions:
          if action.try_execute(grid, turn, ship):
            return True
    return False
