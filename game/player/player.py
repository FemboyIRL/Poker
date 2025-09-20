from enum import Enum
from typing import List


class PlayerStatus(Enum):
    ACTIVE = "active"
    FOLDED = "folded"
    ALL_IN = "all-in"
    OUT = "out"  # Jugador eliminado del torneo


class Player:
    def __init__(self, player_id: int, name: str, stack: int):
        self.id = player_id
        self.name = name
        self.stack = stack
        self.current_bet = 0
        self.status = PlayerStatus.ACTIVE
        self.is_all_in = False
        self.hole_cards: List[str] = []

    def __repr__(self):
        return (f"Player(id={self.id}, name='{self.name}', stack={self.stack}, "
                f"current_bet={self.current_bet}, status={self.status.name}, "
                f"is_all_in={self.is_all_in}, hole_cards={self.hole_cards})")

    def bet(self, amount: int):
        """El jugador apuesta fichas, ajustando su stack."""
        if amount >= self.stack:
            amount = self.stack
            self.is_all_in = True
        self.stack -= amount
        self.current_bet += amount
        return amount

    def fold(self):
        self.status = PlayerStatus.FOLDED
        self.current_bet = 0
        self.is_all_in = False

    def reset_for_new_round(self):
        self.current_bet = 0
        self.is_all_in = False
