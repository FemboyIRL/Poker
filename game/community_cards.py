from typing import List


class CommunityCards:
    def __init__(self):
        self.cards: List[str] = []

    def add_card(self, card: str):
        if len(self.cards) < 5:
            self.cards.append(card)

    def reset(self):
        self.cards.clear()
