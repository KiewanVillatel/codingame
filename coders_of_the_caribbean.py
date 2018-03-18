import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

grid = []


class Action:
  def can_execute(self, grid, turn, ship_pos):
    pass

  def execute(self):
    pass


class MoveAction(Action):
  def __init__(self, pos):
    self.pos = pos

  def can_execute(self, grid, turn, ship_pos):
    return True

  def execute(self):
    print('MOVE ' + self.pos.to_string())


class MoveToNearestBarrelAction(Action):
  def __init__(self):
    self.previous_target_barrel = None

  def can_execute(self, grid, turn, ship_pos):
    if self.previous_target_barrel == None or not isinstance(grid.get(self.previous_target_barrel.pos), Barrel):
      self.previous_target_barrel = grid.find_nearest(Barrel, ships[i].pos)
    return self.previous_target_barrel != None

  def execute(self):
    MoveAction(self.previous_target_barrel.pos).execute()


class ShotNearestEnemyAction(Action):
  def __init__(self):
    self.last_shot = -99999

  def can_execute(self, grid, turn, ship_pos):
    if turn - self.last_shot <= 2:
      return False
    self.target = grid.find_nearest(Ship, ship_pos, lambda s: not s.owner)
    if ship_pos.dist_to(self.target.pos) > 10:
      return False
    self.last_shot = turn
    return True

  def execute(self):
    print('FIRE ' + self.target.pos.to_string())


class PlaceMineAction(Action):
  def __init__(self):
    self.last_mine = -99999

  def can_execute(self, grid, turn, ship_pos):
    if turn - self.last_mine <= 5:
      return False
    self.last_mine = turn
    return True

  def execute(self):
    print('MINE')


class Pos:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def dist_to(self, pos):
    dx = abs(pos.x - self.x)
    dy = abs(pos.y - self.y)
    return max(dx, dy) - min(dx, dy)

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


actions = [ShotNearestEnemyAction(), MoveToNearestBarrelAction()]
turn = 0
while True:
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
      cell = Ship(pos, arg_1, arg_2, arg_3, arg_4 == 1, entity_id)
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
    for action in actions:
      if action.can_execute(grid, turn, ships[i].pos):
        action.execute()
        break
  turn += 1
