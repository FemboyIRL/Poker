from enum import Enum


class ActionType(Enum):
    FOLD = "fold"
    CALL = "call"
    CHECK = "check"
    RAISE = "raise"


class Action:
    def __init__(self, player_id: int, action_type: ActionType, amount: int = 0):
        self.player_id = player_id
        self.action_type = action_type
        self.amount = amount

    def __repr__(self):
        return f"<Action player={self.player_id} type={self.action_type.value} amount={self.amount}>"
