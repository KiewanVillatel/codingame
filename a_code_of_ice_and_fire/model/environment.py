from .map import Map


class Environment:

  def __init__(self, grid: Map, gold, income, opponent_gold, opponent_income):
    self.map = grid
    self.gold = gold
    self.income = income
    self.opponent_gold = opponent_gold
    self.opponent_income = opponent_income
