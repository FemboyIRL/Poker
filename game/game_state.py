from game.action_history import ActionHistory
from game.community_cards import CommunityCards
from game.deck import create_deck, shuffle_deck
from game.game_info import GameInfo
from game.player.player_manager import PlayerManager
from game.pot.pot_manager import PotManager
from game.utils import PokerPhase


class GameState:
    def __init__(
        self, hand_id: int, dealer_position: int, small_blind: int, big_blind: int
    ):
        self.info = GameInfo(hand_id, dealer_position, small_blind, big_blind)
        self.community_cards = CommunityCards()
        self.pot_manager = PotManager()
        self.player_manager = PlayerManager()
        self.action_history = ActionHistory()
        self.deck = []

        # Numero de rondas transcurridas
        self.round_number = 1

        # ID de la fase actual de la ronda         
        self.phase_round = PokerPhase.PRE_FLOP

        # ID del jugador que tiene el boton(gira a la derecha cada ronda)
        self.current_button_player_id: int = 0 

        # ID del jugador actual que debe tomar decisión
        self.current_player_id: int = None

        # Acciones legales actuales
        self.legal_actions = []

    def start_game(self):
        self.deck = shuffle_deck(create_deck())
        self.phase_round = PokerPhase.PRE_FLOP
        self.run_round()

    def advance_round(self):
        current_value = self.phase_round.value
        next_value = current_value + 1

        # Evita pasar de SHOWDOWN
        if next_value > PokerPhase.SHOWDOWN.value:
            return

        self.phase_round = PokerPhase(next_value)
        self.run_round()

    def ask_player_for_action(self):
        return

    def run_round(self):
        match self.phase_round:
            case PokerPhase.PRE_FLOP:
                print("Repartiendo cartas iniciales...")
                self.run_pre_flop()

            case PokerPhase.FLOP:
                print("Mostrando el Flop...")
                self.run_flop()

            case PokerPhase.TURN:
                print("Mostrando el Turn...")
                self.run_turn()

            case PokerPhase.RIVER:
                print("Mostrando el River...")
                self.run_river()

            case PokerPhase.SHOWDOWN:
                print("Showdown: Determinando ganador...")

    def run_pre_flop(self):
        for _, player in enumerate(self.player_manager.get_active_players()):
            player.hole_cards = [self.deck.pop(), self.deck.pop()]
            print(player)
        self.advance_round()

    def run_flop(self):
        for _ in range(3):
            self.community_cards.add_card(self.deck.pop())
        print(self.community_cards.cards)
        self.advance_round()
    
    def run_turn(self):
        self.community_cards.add_card(self.deck.pop())
        print(self.community_cards.cards)
        self.advance_round()

    def run_river(self):
        self.community_cards.add_card(self.deck.pop())
        print(self.community_cards.cards)
        self.advance_round()

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
