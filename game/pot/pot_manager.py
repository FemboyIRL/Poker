from typing import List

from game.pot.side_pot import SidePot


class PotManager:
    def __init__(self):
        self.side_pots: List[SidePot] = []

    def add_side_pot(self, amount: int, eligible_players: List[int]):
        pot = SidePot(amount)
        pot.eligible_players = eligible_players.copy()
        self.side_pots.append(pot)

    @property
    def total_pot(self):
        return sum(pot.amount for pot in self.side_pots)
