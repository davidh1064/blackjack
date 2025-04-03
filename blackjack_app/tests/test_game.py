import pytest
from blackjack.game import BlackjackGame
from blackjack.models.game_state import GamePhase

@pytest.fixture
def game():
    return BlackjackGame()

def test_initial_state(game):
    assert game.phase == GamePhase.WAITING_FOR_BET
    assert game.player_money == 1000
    assert game.bet == 0
    assert len(game.player_hand.cards) == 0
    assert len(game.dealer_hand.cards) == 0

def test_start_new_round(game):
    game.start_new_round(100)
    assert game.phase == GamePhase.PLAYER_TURN
    assert game.bet == 100
    assert len(game.player_hand.cards) == 2
    assert len(game.dealer_hand.cards) == 2

def test_hit(game):
    game.start_new_round(100)
    initial_cards = len(game.player_hand.cards)
    game.hit()
    assert len(game.player_hand.cards) == initial_cards + 1

def test_stand(game):
    game.start_new_round(100)
    game.stand()
    assert game.phase == GamePhase.ROUND_OVER

def test_blackjack(game):
    # This is a simplified test - in reality, you'd need to rig the deck
    game.start_new_round(100)
    game.player_hand.add_card(game.deck.draw_card())  # Add an Ace
    game.player_hand.add_card(game.deck.draw_card())  # Add a 10
    assert game.player_hand.is_blackjack()

def test_bust(game):
    game.start_new_round(100)
    # Add cards until bust (simplified)
    for _ in range(5):
        game.player_hand.add_card(game.deck.draw_card())
    assert game.player_hand.is_bust() 