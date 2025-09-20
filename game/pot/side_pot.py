from typing import List


class SidePot:
    def __init__(self, amount: int):
        self.amount = amount
        self.eligible_players: List[int] = []

    def add_player(self, player_id: int):
        if player_id not in self.eligible_players:
            self.eligible_players.append(player_id)
