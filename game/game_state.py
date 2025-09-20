from game.action_history import ActionHistory
from game.actions import Action, ActionType
from game.community_cards import CommunityCards
from game.deck import create_deck, shuffle_deck
from game.game_info import GameInfo
from game.player.player import PlayerStatus
from game.player.player_manager import PlayerManager
from game.pot.pot_manager import PotManager
from game.utils import PokerPhase


class GameState:
    def __init__(self, hand_id: int, small_blind: int, big_blind: int):
        self.info = GameInfo(hand_id, small_blind, big_blind)
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
        self.current_button_player_id = 1
        self.phase_round = PokerPhase.PRE_FLOP
        self.run_round()

    def advance_round(self):
        current_value = self.phase_round.value
        next_value = current_value + 1

        # Evita pasar de SHOWDOWN
        if next_value > PokerPhase.SHOWDOWN.value:
            self.phase_round = PokerPhase.PRE_FLOP
            return

        self.phase_round = PokerPhase(next_value)
        self.run_round()

    def run_bet_rounds(self):
        for _, player in enumerate(self.player_manager.get_active_players()):
            action = self.ask_player_for_action(player_id=player.id)
            self.process_action(action=action, player=player)

    def ask_player_for_action(self, player_id):
        return Action(action_type=ActionType.CHECK, amount=200, player_id=player_id)

    def process_action(self, action, player):
        match (action):
            case ActionType.FOLD:
                player.fold()
            case ActionType.CHECK:
                # Check Logic
                return
            case ActionType.CALL:
                # Call Logic
                return

    def run_round(self):

        active_players = self.player_manager.get_active_players()
        if len(active_players) == 1:
            # Logica para poner el ganador de una sin tener que hacer showdown
            return

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
                self.run_showdown()

    def run_pre_flop(self):
        for _, player in enumerate(self.player_manager.get_active_players()):
            player.hole_cards = [self.deck.pop(), self.deck.pop()]
            print(player)
        self.run_bet_rounds()
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

    def run_showdown(self):
        # self.evaluate_hands()
        # self.determine_winners()
        print(self.current_button_player_id)
        self.rotate_button()
        print(self.current_button_player_id)

    def rotate_button(self):
        """
        Mueve el botón al siguiente jugador activo.
        """
        players = self.player_manager.players
        total_players = len(players)

        # Buscar índice actual del botón
        current_index = next(
            (i for i, p in enumerate(players) if p.id == self.current_button_player_id),
            None,
        )

        if current_index is None:
            raise ValueError("El jugador actual con el botón no existe en la lista.")

        # Buscar siguiente jugador activo
        for i in range(1, total_players + 1):
            next_index = (current_index + i) % total_players
            next_player = players[next_index]

            if next_player.status == PlayerStatus.ACTIVE:
                self.current_button_player_id = next_player.id
                return next_player  # Devuelve el jugador que ahora tiene el botón

        raise RuntimeError("No hay jugadores activos para rotar el botón.")

    def to_dict(self, player_id: int):
        """Convierte el estado a un dict seguro para un bot específico."""
        player = next(p for p in self.player_manager.players if p.id == player_id)
        return {
            "hand_id": self.info.hand_id,
            "round_name": self.phase_round.name,
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
