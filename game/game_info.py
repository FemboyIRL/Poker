class GameInfo:
    def __init__(self, hand_id: int, small_blind: int, big_blind: int):
        self.hand_id = hand_id
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.current_bet = 0
        self.min_raise = big_blind
