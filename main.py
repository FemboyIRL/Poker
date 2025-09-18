# Crear estado del juego
from game.actions import Action, ActionType
from game.deck import create_deck, shuffle_deck
from game.game_state import GameState
from game.player.player import Player

state = GameState(hand_id=1, dealer_position=0, small_blind=50, big_blind=100)

# Agregar jugadores
state.player_manager.add_player(Player(1, "Bot_A", 1500))
state.player_manager.add_player(Player(2, "Bot_B", 1500))

deck = shuffle_deck(create_deck())

# Asignar cartas privadas
state.player_manager.players[0].hole_cards = [str(deck.pop()), str(deck.pop())]
state.player_manager.players[1].hole_cards = [str(deck.pop()), str(deck.pop())]

# Agregar cartas comunitarias
state.community_cards.add_card(str(deck.pop()))
state.community_cards.add_card(str(deck.pop()))
state.community_cards.add_card(str(deck.pop()))

# Registrar una acción
state.action_history.add_action(Action(1, ActionType.CALL, 100))
state.action_history.add_action(Action(2, ActionType.RAISE, 200))

# Generar estado seguro para el Bot 1
bot_view = state.to_dict(player_id=1)
bot_view_2 = state.to_dict(player_id=2)

print(bot_view)
print("\n")
print(bot_view_2)
