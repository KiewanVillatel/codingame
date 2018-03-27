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

  def times(self, number):
    return Pos(self.x * number, self.y * number, self.z * number)

  def is_in_direction(self, start_pos, direction):
    dx = self.x - start_pos.x
    dy = self.y - start_pos.y
    dz = self.z - start_pos.z

    for i in range(23):
      temp_pos = start_pos.plus(Pos(i * direction.x, i * direction.y, i * direction.z))
      if temp_pos.x == self.x and temp_pos.y == self.y and temp_pos.z == self.z:
        return True

    return False

  def to_string(self):
    return str(self.x) + " " + str(self.y) + " " + str(self.z)

  def to_oddr_string(self):
    x, y = self.to_oddr()
    return str(x) + " " + str(y)


class Cell:
  def __init__(self, pos, cannonball=None):
    self.pos = pos
    self.cannonball = cannonball


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

  def get_pos_in_line(self):
    cells = []
    for i in range(23):
      cells.append(self.front_pos().plus(Pos(i * self.rotation.x, i * self.rotation.y, i * self.rotation.z)))
    return cells

  def get_next_pos(self):
    return self.pos.plus(self.rotation.times(self.speed))

  def get_next_front_pos(self):
    return self.front_pos().plus(self.rotation.times(self.speed))

  def get_next_back_pos(self):
    return self.back_pos().plus(self.rotation.times(self.speed))


class Barrel(Cell):
  def __init__(self, pos, rum):
    super().__init__(pos)
    self.rum = rum


class Mine(Cell):
  def __init__(self, pos):
    super().__init__(pos)


class Cannonball(Cell):
  def __init__(self, pos, shooter_id, time_before_impact):
    super().__init__(pos)
    self._shooter_id = shooter_id
    self._time_before_impact = time_before_impact


class Grid:
  def __init__(self):
    self.grid = [[Cell(Pos.from_oddr(i, j)) for j in range(21)] for i in range(23)]

  def find_nearest(self, claz, pos, condition=None):
    min_dist = 99999999
    res = None
    for row in self.grid:
      for cell in row:
        dist = pos.dist_to(cell.pos)
        if isinstance(cell, claz) and dist < min_dist and (condition is None or condition(cell)):
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
