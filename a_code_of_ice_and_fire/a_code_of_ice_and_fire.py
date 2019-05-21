import sys

from .agents.bronze_agent import BronzeAgent
from .model.building import Building, BuildingType
from .model.environment import Environment
from .model.map import Map
from .model.unit import Unit

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

mine_spots = {}
number_mine_spots = int(input())
for i in range(number_mine_spots):
  x, y = [int(j) for j in input().split()]
  if x not in mine_spots:
    mine_spots[x] = {}
  mine_spots[x][y] = True



# game loop
while True:

  map = Map()

  gold = int(input())
  income = int(input())
  opponent_gold = int(input())
  opponent_income = int(input())
  for y in range(12):
    line = input()
    # print(line, file=sys.stderr)
    for x, c in enumerate(line):
      cell = map.get_cell(x, y)

      if x in mine_spots and y in mine_spots[x]:
        cell.is_mine_spot = True

      if c == "#":
        cell.is_void, cell.is_owned, cell.is_active, cell.is_neutral = True, False, False, False
      elif c == ".":
        cell.is_void, cell.is_owned, cell.is_active, cell.is_neutral = False, False, False, True
      elif c == "O":
        cell.is_void, cell.is_owned, cell.is_active, cell.is_neutral = False, True, True, False
      elif c == "o":
        cell.is_void, cell.is_owned, cell.is_active, cell.is_neutral = False, True, False, False
      elif c == "X":
        cell.is_void, cell.is_owned, cell.is_active, cell.is_neutral = False, False, True, False
      elif c == "x":
        cell.is_void, cell.is_owned, cell.is_active, cell.is_neutral = False, False, False, False
      else:
        raise Exception("Unable to parse cell")

  building_count = int(input())
  for i in range(building_count):
    owner, building_type, x, y = [int(j) for j in input().split()]
    building_type = BuildingType(building_type)
    building = Building(x=x, y=y, is_owned=owner == 0, type=building_type)
    map.get_cell(x, y).building = building

  unit_count = int(input())
  for i in range(unit_count):
    owner, unit_id, level, x, y = [int(j) for j in input().split()]
    unit = Unit(x=x, y=y, is_owned=owner == 0, unit_id=unit_id, level=level)
    map.get_cell(x, y).unit = unit

  agent = BronzeAgent()

  environment = Environment(grid=map,
                            gold=gold,
                            income=income,
                            opponent_gold=opponent_gold,
                            opponent_income=opponent_income)

  agent.act(environment)

  # Write an action using print
  # To debug: print("Debug messages...", file=sys.stderr)
