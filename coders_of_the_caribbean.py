import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

grid = []


class Pos:
  def __init__(self, x, y):
    self.x = x
    self.y = y


class Cell:
  def __init__(self, pos):
    self.pos = pos


class Ship(Cell):
  def __init__(self, pos, rotation, speed, rum, owner):
    super().__init__(pos)
    self.rotation = rotation
    self.speed = speed
    self.rum = rum
    self.owner = owner


class Barrel(Cell):
  def __init__(self, pos, rum):
    super().__init__(pos)
    self.rum = rum


grid = [[Cell(Pos(i, j)) for j in range(21)] for i in range(23)]

# game loop
while True:
  my_ship_count = int(input())  # the number of remaining ships
  entity_count = int(input())  # the number of entities (e.g. ships, mines or cannonballs)
  for i in range(entity_count):
    entity_id, entity_type, x, y, arg_1, arg_2, arg_3, arg_4 = input().split()
    entity_id = int(entity_id)
    x = int(x)
    y = int(y)
    arg_1 = int(arg_1)
    arg_2 = int(arg_2)
    arg_3 = int(arg_3)
    arg_4 = int(arg_4)

    if entity_type == 'SHIP':
      grid[x][y] = Ship(Pos(x, y), arg_1, arg_2, arg_3, arg_4 == 0)
    else:
      grid[x][y] = Barrel(Pos(x, y), arg_1)

  for i in range(my_ship_count):
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Any valid action, such as "WAIT" or "MOVE x y"
    print("MOVE 11 10")
