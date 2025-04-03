from enum import Enum

class GamePhase(Enum):
    WAITING_FOR_BET = "waiting_for_bet"
    PLAYER_TURN = "player_turn"
    DEALER_TURN = "dealer_turn"
    ROUND_OVER = "round_over" 