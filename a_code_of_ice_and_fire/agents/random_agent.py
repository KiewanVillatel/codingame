from ..model.map import Map
import random


class RandomAgent:

    def act(self, map: Map):
        orders = []

        owned_units = map.get_owned_units()

        for unit in owned_units:
            adjacent_cells = map.get_adjacent_cells(unit)

            target_cell = random.choice(adjacent_cells)

            orders.append(' '.join(['MOVE', unit.id, str(target_cell.x), str(target_cell.y)]))

        orders.append('WAIT')
        print(' ;'.join(orders))
