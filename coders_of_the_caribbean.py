import sys
import math
import random


def iround(x):
  """iround(number) -> integer
  Round a number to the nearest integer."""
  return int(round(x) - .5) + (x > 0)

grid = []


class Action:
  def can_execute(self, grid, turn, ship):
    pass

  def execute(self, grid, turn, ship):
    pass


class MoveAction(Action):
  def __init__(self, pos):
    self.pos = pos

  def can_execute(self, grid, turn, ship):
    return True

  def execute(self, grid, turn, ship):
    print('MOVE ' + self.pos.to_string())


class MoveToNearestBarrelAction(Action):
  def can_execute(self, grid, turn, ship):
    if ship.id not in ship_last_barrels or not isinstance(grid.get(ship_last_barrels[ship.id].pos), Barrel):
      nearest_barrel = grid.find_nearest(Barrel, ship.pos, lambda b: b not in ship_last_barrels)
      if nearest_barrel is None:
        return False
      ship_last_barrels[ship.id] = nearest_barrel
    return True

  def execute(self, grid, turn, ship):
    MoveAction(ship_last_barrels[ship.id].pos).execute(grid, turn, ship)

class MoveToNearestEnemyAction(Action):
  def __init__(self):
    self.previous_target_enemy = None

  def can_execute(self, grid, turn, ship):
    if self.previous_target_enemy == None or not isinstance(grid.get(self.previous_target_enemy.pos), Ship):
      self.previous_target_enemy = grid.find_nearest(Ship, ship.pos, lambda s: not s.owner)
    return self.previous_target_enemy != None

  def execute(self, grid, turn, ship):
    MoveAction(self.previous_target_enemy.pos).execute(grid, turn, ship)

class RandomMove(Action):
  def can_execute(self, grid, turn, ship):
    return True

  def execute(self, grid, turn, ship):
    MoveAction(Pos(random.randint(0, 19), random.randint(0, 19))).execute(grid, turn, ship)

class FireAction(Action):
  def __init__(self, target):
    self._target = target

  def can_execute(self, grid, turn, ship):
    if ship.id in ship_last_shots and turn - ship_last_shots[ship.id] <= 2:
      return False

    if not grid.in_grid(self._target.pos):
      return False

    return True

  def execute(self, grid, turn, ship):
    ship_last_shots[ship.id] = turn
    print('FIRE ' + self._target.pos.to_string())

class ShotNearestEnemyAction(Action):
  def can_execute(self, grid, turn, ship):
    if ship.id in ship_last_shots and turn - ship_last_shots[ship.id] <= 2:
      return False
    target = grid.find_nearest(Ship, ship.pos, lambda s: not s.owner)

    if target is None:
      return False

    self.target = None
    for i in range(3):
      target_x = target.pos.x + (i+1) * target.speed * target.rotation.x
      target_y = target.pos.y + (i+1) * target.speed * target.rotation.y
      target_pos = Pos(target_x, target_y)
      t_shot = 1 + iround(target_pos.dist_to(ship.front_pos()) / 3)
      if t_shot - i < 2 and grid.in_grid(target_pos):
        self.target = grid.get(Pos(target_x, target_y))
        break

    if self.target is None:
      return False

    if ship.front_pos().dist_to(self.target.pos) > 10:
      return False

    print('shot', target.pos.to_string(), target.rotation.to_string(), self.target.pos.to_string(), file=sys.stderr)
    return True

  def execute(self, grid, turn, ship):
    ship_last_shots[ship.id] = turn
    print('FIRE ' + self.target.pos.to_string())


class PlaceMineAction(Action):
  def __init__(self):
    self.last_mine = -99999

  def can_execute(self, grid, turn, ship):
    if turn - self.last_mine <= 5:
      return False
    self.last_mine = turn
    return True

  def execute(self, grid, turn, ship):
    print('MINE')


class Pos:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def dist_to(self, pos):
    dx = abs(pos.x - self.x)
    dy = abs(pos.y - self.y)
    return max(dx, dy)

  def plus(self, pos):
    return Pos(self.x + pos.x, self.y + pos.y)

  def minus(self, pos):
    return Pos(self.x - pos.x, self.y - pos.y)

  def to_string(self):
    return str(self.x) + " " + str(self.y)


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
    self.grid = [[Cell(Pos(i, j)) for j in range(21)] for i in range(23)]

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
    return self.grid[pos.x][pos.y]

  def update(self, pos, cell):
    self.grid[pos.x][pos.y] = cell

  def in_grid(self, pos):
    return pos.x < 23 and pos.x >=0 and pos.y <21 and pos.y >=0


def direction_to_pos(dir):
  dx = 1 if dir in [1, 0, 5] else -1
  dy = 1 if dir in [4, 5] else -1 if dir in [2, 1] else 0
  return Pos(dx, dy)


actions = [[ShotNearestEnemyAction(), MoveToNearestBarrelAction(), MoveToNearestEnemyAction(), RandomMove()] for _ in range(3)]
turn = 0
ship_last_barrels = {}
ship_last_shots = {}
while True:
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
    pos = Pos(x, y)
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
      if action.can_execute(grid, turn, ships[i]):
        action.execute(grid, turn, ships[i])
        action_found = True
        break
    print('No action found', file=sys.stderr) if not action_found else None
  turn += 1
