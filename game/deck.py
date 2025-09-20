import random


class Card:
    def __init__(self, value, rank, suit):
        self.value = value
        self.rank = rank
        self.suit = suit
        self.fullname = f"{rank} de {suit}"

    def __str__(self):
        return self.fullname
    
    def __repr__(self):
        return self.__str__()

def create_deck():
    deck = []

    suits = ("Corazones", "Diamantes", "Picas", "Espadas")

    ranks = ("Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")

    for suit in suits:
        for i, rank in enumerate(ranks):
            deck.append(Card(i + 2, rank, suit))

    return deck


def shuffle_deck(deck):
    random.shuffle(deck)
    return deck
