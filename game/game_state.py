from game.action_history import ActionHistory
from game.community_cards import CommunityCards
from game.game_info import GameInfo
from game.player.player_manager import PlayerManager
from game.pot.pot_manager import PotManager


class GameState:
    def __init__(
        self, hand_id: int, dealer_position: int, small_blind: int, big_blind: int
    ):
        self.info = GameInfo(hand_id, dealer_position, small_blind, big_blind)
        self.community_cards = CommunityCards()
        self.pot_manager = PotManager()
        self.player_manager = PlayerManager()
        self.action_history = ActionHistory()

        # ID del jugador actual que debe tomar decisión
        self.current_player_id: int = None

        # Acciones legales actuales
        self.legal_actions = []

    def to_dict(self, player_id: int):
        """Convierte el estado a un dict seguro para un bot específico."""
        player = next(p for p in self.player_manager.players if p.id == player_id)
        return {
            "hand_id": self.info.hand_id,
            "round_name": self.info.round_name,
            "dealer_position": self.info.dealer_position,
            "small_blind": self.info.small_blind,
            "big_blind": self.info.big_blind,
            "pot": self.pot_manager.total_pot,
            "current_bet": self.info.current_bet,
            "min_raise": self.info.min_raise,
            "community_cards": self.community_cards.cards,
            "players": [
                {
                    "id": p.id,
                    "name": p.name,
                    "stack": p.stack,
                    "current_bet": p.current_bet,
                    "status": p.status.value,
                    "is_all_in": p.is_all_in,
                }
                for p in self.player_manager.players
            ],
            "player_id": player.id,
            "hole_cards": player.hole_cards,
            "legal_actions": self.legal_actions,
            "pot_distribution": [
                {"amount": pot.amount, "eligible_players": pot.eligible_players}
                for pot in self.pot_manager.side_pots
            ],
            "last_actions": [
                {
                    "player_id": a.player_id,
                    "action": a.action_type.value,
                    "amount": a.amount,
                }
                for a in self.action_history.get_last_actions(5)
            ],
        }
