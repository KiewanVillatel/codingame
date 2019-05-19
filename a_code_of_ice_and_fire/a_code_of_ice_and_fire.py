import sys
import math
from .model.map import Map
from .model.unit import Unit
from .agents.random_agent import RandomAgent

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

number_mine_spots = int(input())
for i in range(number_mine_spots):
    x, y = [int(j) for j in input().split()]

# game loop
while True:

    map = Map()

    gold = int(input())
    income = int(input())
    opponent_gold = int(input())
    opponent_income = int(input())
    for i in range(12):
        line = input()
        for j, c in enumerate(line):
            cell = map._grid[i][j]
            if c == "#":
                cell.is_void, cell.is_owned, cell.is_active = True, False, False
            elif c == ".":
                cell.is_void, cell.is_owned, cell.is_active = False, False, False
            elif c == "O":
                cell.is_void, cell.is_owned, cell.is_active = False, True, True
            elif c == "o":
                cell.is_void, cell.is_owned, cell.is_active = False, True, False
            elif c == "X":
                cell.is_void, cell.is_owned, cell.is_active = False, False, True
            elif c == "x":
                cell.is_void, cell.is_owned, cell.is_active = False, False, False
            else:
                raise Exception("Unable to parse cell")

    building_count = int(input())
    for i in range(building_count):
        owner, building_type, x, y = [int(j) for j in input().split()]
    unit_count = int(input())
    for i in range(unit_count):
        owner, unit_id, level, x, y = [int(j) for j in input().split()]
        unit = Unit(x=x, y=y, is_owned=owner == 0, unit_id=unit_id, level=level)
        map._grid[x][y].unit = unit

    agent = RandomAgent()

    agent.act(map)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)