from typing import List
from game.player.player import Player, PlayerStatus


class PlayerManager:
    def __init__(self):
        self.players: List[Player] = []

    def add_player(self, player: Player):
        self.players.append(player)

    def get_active_players(self) -> List[Player]:
        return [p for p in self.players if p.status == PlayerStatus.ACTIVE]

    def reset_bets(self):
        for player in self.players:
            player.current_bet = 0
