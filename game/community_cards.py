from typing import List

from game.deck import Card


class CommunityCards:
    def __init__(self):
        self.cards: List[Card] = []

    def add_card(self, card: Card):
        if len(self.cards) < 5:
            self.cards.append(card)

    def reset(self):
        self.cards.clear()
