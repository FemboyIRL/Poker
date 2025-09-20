from typing import List

from game.actions import Action


class ActionHistory:
    def __init__(self):
        self.actions: List[Action] = []

    def add_action(self, action: Action):
        self.actions.append(action)

    def get_last_actions(self, count: int = 5) -> List[Action]:
        return self.actions[-count:]
