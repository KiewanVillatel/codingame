import random

from ..model.environment import Environment


class RandomAgent:

    def act(self, environment: Environment):
        orders = []

        if environment.gold > 10:
            orders.append("TRAIN 1 1 0")

        owned_units = environment.map.get_owned_units()

        for unit in owned_units:
            adjacent_cells = environment.map.get_adjacent_cells(unit)

            if len(adjacent_cells):
                target_cell = random.choice(adjacent_cells)
                orders.append(" ".join(["MOVE", str(unit.id), str(target_cell.x), str(target_cell.y)]))

        orders.append("WAIT")
        print(" ;".join(orders))
