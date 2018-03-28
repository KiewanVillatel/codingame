import heapq


class ACell:
  def __init__(self, cell, g, h, path):
    self._cell = cell
    self._g = g
    self._h = h
    self._f = self._g + self._h
    self._path = path

  def __lt__(self, other):
    return self._f < other._f


class AStar:
  def __init__(self, heuristic, get_adjacent_cells, compare):
    self._heuristic = heuristic
    self._get_adjacent_cells = get_adjacent_cells
    self._target = None
    self._queue = []
    self._compare = compare

  def find_path(self, start_pos, target_pos):
    self._target = target_pos
    h = self._heuristic(start_pos, target_pos)
    heapq.heappush(self._queue, ACell(start_pos, 0, h, []))

    result = self.run()

    if result is None:
      return None

    return result

  def run(self):
    start_acell = heapq.heappop(self._queue)
    adjacent_cells = self._get_adjacent_cells(start_acell._cell)

    new_g = start_acell._g + 1

    for cell in adjacent_cells:
      new_path = start_acell._path + [cell]
      if self._compare(cell, self._target):
        return new_path, new_g
      new_h = self._heuristic(cell, self._target)
      heapq.heappush(self._queue, ACell(cell, new_g, new_h, new_path))

    return self.run()


class DemoCell:
  def __init__(self, x, y):
    self.x = x
    self.y = y


def adjacent_cells(cell):
  x = cell.x
  y = cell.y
  return [DemoCell(x - 1, y), DemoCell(x + 1, y), DemoCell(x, y - 1), DemoCell(x, y + 1)]


def heuristic(c1, c2):
  return (c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2

def compare(c1, c2):
  return c1.x == c2.x and c1.y == c2.y


#print(AStar(heuristic, adjacent_cells, compare).find_path(Cell(0, 0), Cell(10, 10)))
