# Crear estado del juego
from game.actions import Action, ActionType
from game.deck import create_deck, shuffle_deck
from game.game_state import GameState
from game.player.player import Player

state = GameState(hand_id=1, small_blind=50, big_blind=100)

# Agregar jugadores
state.player_manager.add_player(Player(1, "Cheems", 20000))
state.player_manager.add_player(Player(2, "Marcelo", 1500))
state.player_manager.add_player(Player(3, "Joaquin", 1500))
state.player_manager.add_player(Player(4, "Gonzalo", 1500))

state.start_game()

# Registrar una acción
state.action_history.add_action(Action(1, ActionType.CALL, 100))
state.action_history.add_action(Action(2, ActionType.RAISE, 200))

# Generar estado seguro para el Bot 1
bot_view = state.to_dict(player_id=1)
bot_view_2 = state.to_dict(player_id=2)

# print(bot_view)
# print("\n")
# print(bot_view_2)
