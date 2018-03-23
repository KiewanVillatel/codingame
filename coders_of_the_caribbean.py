import sys
import math
import random


def iround(x):
  """iround(number) -> integer
  Round a number to the nearest integer."""
  return int(round(x) - .5) + (x > 0)


grid = []


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
  def __init__(self):
    self._last_accelerate = -99999

  def try_execute(self, grid, turn, ship):
    # if turn - self._last_accelerate <= 3:
    #   return False
    if ship.speed != 1:
      return False
    if ship.id not in ships_target_pos:
      return False
    target_pos = ships_target_pos[ship.id]
    if not target_pos.is_in_direction(ship.pos, ship.rotation):
      return False
    self._last_accelerate = turn
    print('FASTER')
    return True


class PlaceMineAction(Action):
  def __init__(self):
    self.last_mine = -99999

  def try_execute(self, grid, turn, ship):
    if turn - self.last_mine <= 5:
      return False
    self.last_mine = turn
    print('MINE')
    return True


class Pos:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  @staticmethod
  def from_oddr(col, row):
    x = col - (row - (row & 1)) // 2
    z = row
    y = -x - z
    return Pos(x, y, z)

  def to_oddr(self):
    col = self.x + (self.z - (self.z & 1)) // 2
    row = self.z
    return col, row

  def dist_to(self, pos):
    return (abs(self.x - pos.x) + abs(self.y - pos.y) + abs(self.z - pos.z)) // 2

  def plus(self, pos):
    return Pos(self.x + pos.x, self.y + pos.y, self.z + pos.z)

  def minus(self, pos):
    return Pos(self.x - pos.x, self.y - pos.y, self.z - pos.z)

  def is_in_direction(self, start_pos, direction):
    dx = self.x - start_pos.x
    dy = self.y - start_pos.y
    dz = self.z - start_pos.z

    for i in range(23):
      temp_pos = start_pos.plus(Pos(i*direction.x, i*direction.y, i*direction.z))
      if temp_pos.x == self.x and temp_pos.y == self.y and temp_pos.z == self.z:
        return True

    return False

  def to_string(self):
    return str(self.x) + " " + str(self.y) + " " + str(self.z)

  def to_oddr_string(self):
    x, y = self.to_oddr()
    return str(x) + " " + str(y)


class Cell:
  def __init__(self, pos):
    self.pos = pos


class Ship(Cell):
  def __init__(self, pos, rotation, speed, rum, owner, id):
    super().__init__(pos)
    self.rotation = rotation
    self.speed = speed
    self.rum = rum
    self.owner = owner
    self.id = id

  def front_pos(self):
    return self.pos.plus(self.rotation)

  def back_pos(self):
    return self.pos.minus(self.rotation)


class Barrel(Cell):
  def __init__(self, pos, rum):
    super().__init__(pos)
    self.rum = rum


class Mine(Cell):
  def __init__(self, pos):
    super().__init__(pos)


class Grid:
  def __init__(self):
    self.grid = [[Cell(Pos.from_oddr(i, j)) for j in range(21)] for i in range(23)]

  def find_nearest(self, claz, pos, condition=None):
    min_dist = 99999999
    res = None
    for row in self.grid:
      for cell in row:
        dist = pos.dist_to(cell.pos)
        if isinstance(cell, claz) and dist < min_dist and (condition == None or condition(cell)):
          res = cell
          min_dist = dist
    return res

  def get(self, pos):
    x, y = pos.to_oddr()
    return self.grid[x][y]

  def update(self, pos, cell):
    x, y = pos.to_oddr()
    self.grid[x][y] = cell

  def in_grid(self, pos):
    x, y = pos.to_oddr()
    return x < 23 and x >= 0 and y < 21 and y >= 0


def direction_to_pos(dir):
  dir_map = {
    0: Pos(1, -1, 0),
    1: Pos(1, 0, -1),
    2: Pos(0, 1, -1),
    3: Pos(-1, 1, 0),
    4: Pos(-1, 0, 1),
    5: Pos(0, -1, 1),
  }
  return dir_map[dir]


actions = [
  [ShotTargetedEnemyAction(), ShotNearestEnemyAction(), ShotMineAction(), Accelerate(), MoveToNearestBarrelAction(), MoveToTargetedShip(0), MoveToNearestEnemyAction(),
   RandomMove()] for _ in range(3)]
# actions = [[ShotNearestEnemyAction(), MoveToNearestBarrelAction()] for _ in range(3)]
turn = 0
ship_last_barrels = {}
ship_last_shots = {}
ships_target_pos = {}
while True:
  targeted_ships = []
  targeted_barrels = []
  ships = {}
  grid = Grid()
  my_ship_count = int(input())  # the number of remaining ships
  entity_count = int(input())  # the number of entities (e.g. ships, mines or cannonballs)
  for i in range(entity_count):
    entity_id, entity_type, x, y, arg_1, arg_2, arg_3, arg_4 = input().split()
    entity_id = int(entity_id)
    x = int(x)
    y = int(y)
    pos = Pos.from_oddr(x, y)
    print(pos.to_string(), x, y, file=sys.stderr)
    arg_1 = int(arg_1)
    arg_2 = int(arg_2)
    arg_3 = int(arg_3)
    arg_4 = int(arg_4)

    if entity_type == 'SHIP':
      cell = Ship(pos, direction_to_pos(arg_1), arg_2, arg_3, arg_4 == 1, entity_id)
      ships[i] = cell
    elif entity_type == 'MINE':
      cell = Mine(pos)
    elif entity_type == 'BARREL':
      cell = Barrel(pos, arg_1)
    else:
      cell = Cell(pos)

    grid.update(pos, cell)

  for i in range(my_ship_count):
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Any valid action, such as "WAIT" or "MOVE x y"
    print(ships[i].pos.to_string(), file=sys.stderr)

    action_found = False
    for action in actions[i]:
      if action.try_execute(grid, turn, ships[i]):
        action_found = True
        break
    print('No action found', file=sys.stderr) if not action_found else None
  turn += 1
