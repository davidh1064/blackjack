import logging
from typing import Optional
from .models.card import Card
from .models.deck import Deck
from .models.hand import Hand
from .models.game_state import GamePhase

logger = logging.getLogger(__name__)

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.phase = GamePhase.WAITING_FOR_BET
        self.bet = 0
        self.message = ""
        self.player_money = 1000  # Starting money

    def start_new_round(self, bet: int) -> None:
        if bet > self.player_money:
            raise ValueError("Bet cannot exceed player's money")
        
        self.bet = bet
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.phase = GamePhase.PLAYER_TURN
        
        # Deal initial cards
        self.player_hand.add_card(self.deck.draw_card())
        self.dealer_hand.add_card(self.deck.draw_card())
        self.player_hand.add_card(self.deck.draw_card())
        self.dealer_hand.add_card(self.deck.draw_card())
        
        logger.info(f"Started new round with bet: {bet}")

    def hit(self) -> None:
        if self.phase != GamePhase.PLAYER_TURN:
            raise ValueError("Cannot hit at this phase")
        
        self.player_hand.add_card(self.deck.draw_card())
        logger.info(f"Player hit. New hand value: {self.player_hand.get_value()}")
        
        if self.player_hand.is_bust():
            self.phase = GamePhase.ROUND_OVER
            self.message = "Bust! You lose!"
            self.player_money -= self.bet
            logger.info("Player busted")

    def stand(self) -> None:
        if self.phase != GamePhase.PLAYER_TURN:
            raise ValueError("Cannot stand at this phase")
        
        self.phase = GamePhase.DEALER_TURN
        logger.info("Player stood")
        
        # Dealer's turn
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.draw_card())
            logger.info(f"Dealer hit. New hand value: {self.dealer_hand.get_value()}")
        
        self.phase = GamePhase.ROUND_OVER
        self._determine_winner()

    def _determine_winner(self) -> None:
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        if self.player_hand.is_blackjack():
            self.message = "Blackjack! You win!"
            self.player_money += int(self.bet * 1.5)
            logger.info("Player won with blackjack")
        elif self.dealer_hand.is_blackjack():
            self.message = "Dealer has Blackjack! You lose!"
            self.player_money -= self.bet
            logger.info("Dealer won with blackjack")
        elif self.dealer_hand.is_bust():
            self.message = "Dealer busts! You win!"
            self.player_money += self.bet
            logger.info("Dealer busted, player won")
        elif player_value > dealer_value:
            self.message = "You win!"
            self.player_money += self.bet
            logger.info("Player won with higher value")
        elif player_value < dealer_value:
            self.message = "Dealer wins!"
            self.player_money -= self.bet
            logger.info("Dealer won with higher value")
        else:
            self.message = "Push!"
            logger.info("Round ended in push")

    def get_state(self) -> dict:
        return {
            "phase": self.phase.value,
            "player_hand": str(self.player_hand),
            "dealer_hand": str(self.dealer_hand),
            "player_value": self.player_hand.get_value(),
            "dealer_value": self.dealer_hand.get_value(),
            "message": self.message,
            "player_money": self.player_money,
            "bet": self.bet
        } 