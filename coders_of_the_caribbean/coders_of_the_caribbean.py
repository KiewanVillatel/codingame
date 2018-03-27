import sys

from .actions.actions import AvoidCannonballAction, StopIfMine, ShotTargetedEnemyAction, ShotNearestEnemyAction, ShotMineAction, Accelerate, MoveToNearestBarrelAction, MoveToTargetedShip, MoveToNearestEnemyAction, PlaceMineAction, RandomMove
from .model.model import Grid, Pos, Mine, Barrel, Ship, Cell, Cannonball
from .global_vars import targeted_ships, targeted_barrels, cannonballs

grid = []


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
  [StopIfMine(), AvoidCannonballAction(), ShotTargetedEnemyAction(), ShotNearestEnemyAction(), ShotMineAction(), Accelerate(), MoveToNearestBarrelAction(),
   MoveToTargetedShip(), MoveToNearestEnemyAction(), PlaceMineAction(), RandomMove()] for _ in range(3)]

turn = 0
while True:
  targeted_ships.clear()
  targeted_barrels.clear()
  cannonballs.clear()

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
    elif entity_type == 'CANNONBALL':
      cell = Cannonball(pos, arg_1, arg_2)
      cannonballs.append(cell)
    else:
      cell = Cell(pos)

    grid.update(pos, cell)

  for cannonball in cannonballs:
    grid.get(cannonball.pos).cannonball = cannonball

  for i in range(my_ship_count):
    action_found = False
    for action in actions[i]:
      if action.try_execute(grid, turn, ships[i]):
        action_found = True
        break
    print('No action found', file=sys.stderr) if not action_found else None
  turn += 1
